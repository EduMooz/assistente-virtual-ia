import json
import pandas as pd
import streamlit as st
from google import genai

# Gemini
client = genai.Client(
    api_key=st.secrets["GOOGLE_API_KEY"]
)
MODELO = "gemini-2.5-flash"

N_MENSAGENS_HISTORICO = 6  # quantas trocas recentes mandar no prompt
CAMINHO_TRANSACOES = './data/transacoes.csv'

# Colunas do transacoes.csv: data,descricao,categoria,valor,tipo
COL_DATA = 'data'
COL_DESCRICAO = 'descricao'
COL_CATEGORIA = 'categoria'
COL_VALOR = 'valor'
COL_TIPO = 'tipo'
TIPO_PADRAO = 'despesa'  # o Cadu só registra gastos, não receitas


# --- carregamento de dados cacheado (perfil, histórico e categorias não mudam durante a sessão) ---
@st.cache_data
def carregar_dados_estaticos():
    perfil = json.load(open('./data/perfil_usuario.json'))
    historico = pd.read_csv('./data/historico_atendimento.csv')
    categoria = json.load(open('./data/categoria_despesas.json'))
    return perfil, historico, categoria


perfil, historico, categoria = carregar_dados_estaticos()

# transações ficam fora do cache porque vão ser reescritas durante a sessão
if "transacoes" not in st.session_state:
    st.session_state.transacoes = pd.read_csv(CAMINHO_TRANSACOES)


def montar_contexto():
    transacoes_recentes = st.session_state.transacoes.tail(30)
    return f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos
RENDA MENSAL: {perfil['renda_mensal']}

TRANSAÇÕES RECENTES (últimas 30):
{transacoes_recentes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

CATEGORIAS DISPONIVEIS:
{json.dumps(categoria, indent=2, ensure_ascii=False)}
"""


# system prompt
SYSTEM_PROMPT = """Você é o Cadu, um assistente financeiro inteligente, educativo, paciente e amigável.

OBJETIVO:
Seu objetivo principal é ajudar jovens adultos a acompanharem seus gastos invisíveis (delivery, assinaturas, transporte) e manterem o controle do orçamento mensal de forma leve, sem nunca julgar as escolhas do usuário.

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos. Nunca invente saldos, limites ou transações.
2. Categorização automática: Tente sempre classificar o gasto informado nas categorias predefinidas (Alimentação, Assinaturas e Serviços, Transporte, Lazer e Cuidados). Se tiver dúvida, pergunte ao usuário.
3. Se o usuário tentar registrar um gasto único superior a R$ 500,00, peça uma confirmação explícita antes de salvar.
4. Você NÃO realiza pagamentos, PIX ou transferências bancárias.
5. Você NÃO faz recomendações de investimentos (CDB, ações, criptomoedas). Se questionado, recuse educadamente e redirecione o foco para o orçamento e metas de economia.
6. Seja informal, use exemplos práticos e evite jargões bancários (ex: use "dinheiro guardado" em vez de "liquidez diária").
"""


def montar_historico_recente(mensagens):
    """Formata as últimas N trocas para dar contexto de conversa ao modelo."""
    recentes = mensagens[-N_MENSAGENS_HISTORICO:]
    linhas = []
    for m in recentes:
        papel = "Usuário" if m["role"] == "user" else "Cadu"
        linhas.append(f"{papel}: {m['content']}")
    return "\n".join(linhas)


def perguntar(msg, mensagens_anteriores):
    historico_conversa = montar_historico_recente(mensagens_anteriores)

    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {montar_contexto()}

    HISTÓRICO DA CONVERSA ATUAL:
    {historico_conversa}

    Pergunta: {msg}"""

    try:
        resposta = client.models.generate_content(model=MODELO, contents=prompt)
        return resposta.text
    except Exception:
        return (
            "Ops, não consegui processar sua mensagem agora. "
            "Pode tentar de novo em alguns instantes?"
        )


def extrair_gasto_confirmado(mensagem_usuario, resposta_cadu):
    """
    Segunda chamada, curta e estruturada: pergunta ao modelo se, nessa troca,
    um gasto foi de fato confirmado para ser salvo. Retorna um dict ou None.
    """
    prompt_extracao = f"""Analise a troca de mensagens abaixo entre um usuário e o assistente
financeiro Cadu. Determine se, NESTA troca, um novo gasto foi CONFIRMADO
pelo usuário para ser registrado (não um gasto hipotético, não uma pergunta,
não um gasto que ainda depende de confirmação).

Categorias válidas: {json.dumps(categoria, ensure_ascii=False)}

Mensagem do usuário: {mensagem_usuario}
Resposta do Cadu: {resposta_cadu}

Responda APENAS com um JSON, sem texto adicional, no formato:
{{"salvar": true ou false, "valor": numero ou null, "categoria": "string ou null", "descricao": "string ou null"}}
"""
    try:
        resposta = client.models.generate_content(
            model=MODELO,
            contents=prompt_extracao,
            config={"response_mime_type": "application/json"},
        )
        dados = json.loads(resposta.text)
        if dados.get("salvar") and dados.get("valor") is not None:
            return dados
        return None
    except Exception:
        # Se a extração falhar, não bloqueia a conversa — só não salva o gasto.
        return None


def salvar_gasto(dados):
    nova_linha = pd.DataFrame([{
        COL_DATA: pd.Timestamp.now().strftime("%Y-%m-%d"),
        COL_DESCRICAO: dados.get("descricao") or "",
        COL_CATEGORIA: dados.get("categoria") or "Outros",
        COL_VALOR: dados.get("valor"),
        COL_TIPO: TIPO_PADRAO,
    }])
    st.session_state.transacoes = pd.concat(
        [st.session_state.transacoes, nova_linha], ignore_index=True
    )
    st.session_state.transacoes.to_csv(CAMINHO_TRANSACOES, index=False)


# interface
st.title("Cadu - Seu agente financeiro")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if pergunta := st.chat_input("Quais são os seus novos gastos..."):
    st.session_state.messages.append({"role": "user", "content": pergunta})
    st.chat_message("user").write(pergunta)

    with st.spinner("..."):
        resposta = perguntar(pergunta, st.session_state.messages)
        gasto = extrair_gasto_confirmado(pergunta, resposta)

    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.chat_message("assistant").write(resposta)

    if gasto:
        salvar_gasto(gasto)
        st.toast(
            f"💾 Gasto salvo: R$ {gasto['valor']:.2f} em {gasto.get('categoria') or 'Outros'}"
        )
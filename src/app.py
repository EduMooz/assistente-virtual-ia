import json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai
import os

#Gemini
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODELO = "gemini-2.5-flash"

#carregar dados
perfil = json.load(open('./data/perfil_usuario.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
categoria = json.load(open('./data/categoria_despesas.json'))

#montando contexto
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos
RENDA MENSAL: {perfil['renda_mensal']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

CATEGORIAS DISPONIVEIS:
{json.dumps(categoria, indent=2, ensure_ascii=False)}
"""

#system prompt
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

#chamando o ollama
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    resposta = client.models.generate_content(model=MODELO, contents=prompt)
    return resposta.text

#interface
st.title("Cadu - Seu agente financeiro")

if pergunta := st.chat_input("Quais são os seus novos gastos..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
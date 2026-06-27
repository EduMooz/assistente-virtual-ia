# 💰 CADU — Seu Educador Financeiro com IA

> Agente inteligente que ajuda jovens adultos a controlar gastos invisíveis (delivery, assinaturas, transporte) de forma leve e sem julgamentos.

---

## O que é o CADU?

O **CADU** é um assistente financeiro conversacional desenvolvido com IA Generativa. Ele não recomenda investimentos — ele **educa**. O usuário registra gastos via mensagem, o Cadu categoriza automaticamente e envia alertas de orçamento quando necessário.

**Público-alvo:** Jovens adultos e profissionais que querem organizar as finanças pelo celular, mas têm preguiça de planilhas.

---

## Funcionalidades

- Registro rápido de gastos via chat
- Categorização automática (Alimentação, Assinaturas, Transporte, Lazer, Cuidados)
- Alertas de limite de orçamento por categoria
- Consulta de gastos por período ou categoria
- Bloqueio total de recomendações de investimentos
- Confirmação antes de registrar valores acima de R$ 500,00

---

## Arquitetura

```
Usuário → Interface (Streamlit) → LLM (Gemini) → Base de Conhecimento (CSV/JSON) → Resposta
```

| Componente | Tecnologia |
|---|---|
| Interface | Streamlit |
| LLM | Google Gemini |
| Base de dados | JSON e CSV mockados (`/data`) |

---

## Estrutura do Repositório

```
📁 assistente-virtual-ia/
├── 📁 data/
│   ├── transacoes.csv
│   ├── historico_atendimento.csv
│   ├── perfil_investidor.json
│   └── produtos_financeiros.json
├── 📁 docs/
│   ├── 01-documentacao-agente.md   # Persona, caso de uso e arquitetura
│   ├── 02-base-conhecimento.md     # Estratégia de dados
│   ├── 03-prompts.md               # System prompt e exemplos de interação
│   ├── 04-metricas.md              # Avaliação e resultados dos testes
│   └── 05-pitch.md                 # Roteiro do pitch
├── 📁 src/
│   └── app.py                      # Aplicação Streamlit
├── 📁 assets/
├── .env.exemplo
└── README.md
```

---

## Como Executar

```bash
# 1. Clone o repositório
git clone https://github.com/EduMooz/assistente-virtual-ia.git
cd assistente-virtual-ia

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure as variáveis de ambiente
cp .env.exemplo .env
# Adicione sua chave de API no arquivo .env

# 4. Execute a aplicação
streamlit run src/app.py
```

---

## Exemplos de Conversa

**Registro de gasto:**
> Usuário: "Pedi um lanche de 45 reais agora."
> Cadu: "Anotado! Lancei R$ 45,00 em 'Alimentação'. Tá no controle!"

**Tentativa de recomendação de investimento:**
> Usuário: "Onde eu invisto meu dinheiro?"
> Cadu: "Isso foge da minha alçada! Sou focado em organização do dia a dia. Quer revisar seus gastos e ver quanto sobrou esse mês?"

---

## Avaliação

Todos os 4 testes documentados em [`docs/04-metricas.md`](docs/04-metricas.md) foram aprovados:

| Teste | Foco | Resultado |
|---|---|---|
| Consulta de gastos | Assertividade | ✅ Correto |
| Recusa de recomendação de investimento | Segurança | ✅ Correto |
| Pergunta fora do escopo | Segurança e Coerência | ✅ Correto |
| Informação inexistente na base | Assertividade | ✅ Correto |

---

## Limitações Declaradas

O CADU **não** realiza pagamentos, PIX ou transferências; não recomenda produtos financeiros; não prevê cenários macroeconômicos; e não armazena senhas ou dados de cartão.

---

## Desenvolvido por

**EduMooz** · Desafio DIO — Agente Financeiro com IA Generativa

[![GitHub](https://img.shields.io/badge/GitHub-EduMooz-181717?logo=github)](https://github.com/EduMooz)

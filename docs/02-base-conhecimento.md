# Base de Conhecimento

> [!TIP]
> **Prompt usado para esta etapa:**
> 
> Organize a base de conhecimento do agente [nome_do_agente] usando os 4 arquivos da pasta `data/` (em anexo). Explique pra que serve cada arquivo e monte um exemplo de contexto formatado que será enviado pro LLM. Preencha o template abaixo.
>
> [cole ou anexe o template `02-base-conhecimento.md` pra contexto]

---

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Para que serve no Cadu |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores ou seja, dar continuidade no atendimento de forma mais eficiente  |
| `perfil_investidor.json` | JSON | Personalizar as explicações sobre os lançamentos, duvidas e necessidades do cliente |
| `produtos_financeiros.json` | JSON | Conhecer os produtos disponiveis para que eles possam ser explicados aos clientes |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente e usar essas informações de forma didádica|

---

## Adaptações nos Dados

- o arquivo de produtos_financeiros.json foi alterado para categoria_despesas.json assim como o conteudo, pois como o foco do agente é lidar com despesas do dia a dia e há uma regra rígida proibindo recomendações de investimentos, manter um arquivo sobre Tesouro Direto e Fundos pode confundir o LLM e gerar alucinações.
- o arquivo perfil_investidor.json foi alterado para perfil_usuario, alem disso, o conteúdo foi alterado para que o LLM não tenha "gatilhos" para falar sobre investimentos.
- o arquivo historico_atendimento.csv representa atendimentos anteriores simulados, usados como contexto de leitura para o agente responder com mais consistência. Nesta versão, é um dado estático (não é atualizado a cada nova conversa); a persistência de histórico real de conversas fica como evolução futura do projeto.

---

## Estratégia de Integração

### Como os dados são carregados?

Existe duas possibilidades, injetar os dados diretamente no prompt (Ctrl C + Ctrl V), ou carregar os arquivos via código, como no exemplo abaixo:

```Python
import json
import pandas as pd

perfil = json.load(open('./data/perfil_usuario.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
catgoria = json.load(open('./data/categoria_despesas.json'))
```

### Como os dados são usados no prompt?

Para simplificar, podemos simplesmente "injetar" os dados em nosso prompt, garantindo que o agente tenha o melhor contexto possivel. Lembrando que, em soluções mais robustas o ideal é que essas informações sejam carregadas dinamicamente para que possamos ganhar flexibilidade.

```
DADOS E PERFIL DO CLIENTE (data/perfil_usuario.csv):
{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.0,
  "dia_pagamento": 5,
  "orcamento_mensal_limites": {
    "alimentacao": 1200.0,
    "assinaturas": 150.0,
    "transporte": 400.0,
    "lazer": 500.0
  },
  "preferencias_alertas": {
    "ativar_alertas": true,
    "avisar_em_percentual": 80
  },
  "metas_de_economia": [
    {
      "meta": "Reduzir gastos com delivery",
      "limite_estipulado": 300.0,
      "frequencia": "mensal"
    },
    {
      "meta": "Juntar para viagem de férias",
      "valor_necessario": 3000.0,
      "prazo": "2026-12"
    }
  ]
}

HISTORICO DE ATENDIMENTO DO CLIENTE (data/historico_atendimento.csv):
data,canal,tema,resumo,resolvido
2025-11-05,chat,Registro de Gasto (Delivery),Cliente registrou gasto rápido com iFood. Cadu categorizou automaticamente como Alimentação e confirmou o saldo.,sim
2025-11-12,chat,Registro de Gasto (Assinatura),Cliente lançou a cobrança mensal da Netflix. Cadu atualizou a base de dados mockada na pasta data.,sim
2025-11-15,chat,Orçamento Semanal,Cadu enviou um alerta proativo sobre o limite restante para gastos na categoria Lazer de forma educativa.,sim
2025-11-20,chat,Confirmação de Gasto Alto,"Cliente tentou registrar um gasto de R$ 600,00. Cadu acionou a estratégia de segurança e pediu confirmação antes de salvar.",sim
2025-11-25,chat,Limitação (Investimento),Cliente perguntou sobre investimentos em CDB. Cadu explicou educadamente que não faz recomendações e ofereceu ajuda para o orçamento.,sim

TRANSAÇÔES DO CLIENTE (data/transacoes.csv):
data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida

CATEGORIAS DISPONIVEIS (data/categoria_despesas.json):
[
  {
    "categoria": "Alimentação",
    "subcategorias": [
      "Delivery",
      "Mercado",
      "Restaurante",
      "Padaria"
    ],
    "limite_alerta": "Avisar quando atingir 80% do limite semanal",
    "dica_cadu": "Sempre que o gasto com delivery apertar, eu te lembro de dar uma olhada na geladeira primeiro!"
  },
  {
    "categoria": "Assinaturas e Serviços",
    "subcategorias": [
      "Streaming",
      "Música",
      "Internet",
      "Software"
    ],
    "limite_alerta": "Avisar se houver cobrança duplicada ou aumento de valor",
    "dica_cadu": "Muitos streamings de uma vez? Vamos revisar o que você realmente tem assistido esse mês."
  },
  {
    "categoria": "Transporte",
    "subcategorias": [
      "Aplicativo",
      "Transporte Público",
      "Combustível"
    ],
    "limite_alerta": "Avisar quando ultrapassar o orçamento semanal",
    "dica_cadu": "As corridas de app estão pesando? Podemos calcular juntos se vale a pena mudar a rota amanhã."
  },
  {
    "categoria": "Lazer e Cuidados",
    "subcategorias": [
      "Cinema",
      "Beleza",
      "Saúde",
      "Jogos"
    ],
    "limite_alerta": "Avisar no fim de semana para controle",
    "dica_cadu": "Cuidar de você é essencial, meu papel é só garantir que o orçamento não fique no vermelho."
  }
]
```

---

## Exemplo de Contexto Montado

O exemplo de contexto montado abaixo, se baseia nos dados originais da base de conhecimento, mas os sintetiza deixando apenas as informações relevantes, otimizando assim o consumo de tokens. Entretanto, vale lembrar que mais importante que economizar tokens é ter todas as informações relevantes disponiveis em seu contexto.

```text
[CONTEXTO DO SISTEMA - ASSISTENTE CADU]
Você está atendendo o seguinte usuário:

INFORMAÇÕES DO USUÁRIO:
- Nome: João Silva
- Renda Mensal: R$ 5.000,00 (Recebe dia 05)
- Metas Ativas: 
  1. Reduzir gastos com delivery (Limite estipulado: R$ 300/mês)
  2. Juntar R$ 3.000,00 para viagem de férias até 12/2026.

STATUS DO ORÇAMENTO (Limites Mensais):
- Alimentação: R$ 1.200,00
- Assinaturas: R$ 150,00
- Transporte: R$ 400,00
- Lazer: R$ 500,00
* Regra de Alerta: Avisar o cliente sempre que o consumo atingir 80% do limite da categoria.

ÚLTIMAS TRANSAÇÕES (Visão Recente):
- 10/10: Restaurante (Alimentação) - R$ 120,00
- 12/10: Uber (Transporte) - R$ 45,00
- 15/10: Conta de Luz (Moradia) - R$ 180,00
- 20/10: Academia (Saúde) - R$ 99,00

ÚLTIMO ATENDIMENTO:
- Data: 25/11/2025
- Resumo: Cliente perguntou sobre investimentos em CDB. Cadu explicou educadamente que não faz recomendações e ofereceu ajuda para o orçamento.
```

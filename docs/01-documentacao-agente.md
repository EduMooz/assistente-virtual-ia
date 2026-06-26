# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

A dificuldade que algumas pessoas possuem em manter o controle de pequenos gastos diarios (delivery, assinaturas)

### Solução
> Como o agente resolve esse problema de forma proativa?

O agente recebe o registro rápido de gastos via mensagem, categoriza automaticamente as despesas e envia alertas semanais mostrando quanto ainda pode ser gasto dentro do orçamento definido.

### Público-Alvo
> Quem vai usar esse agente?

Jovens adultos e profissionais que desejam organizar as finanças pelo celular, mas têm preguiça ou dificuldade de usar planilhas complexas.

---

## Persona e Tom de Voz

### Nome do Agente
Cadu (Financeiro)

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

- Educativo e paciente
- Usa exemplos praticos
- Nunca julga os gastos do cliente

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Informal e acessível. Evita jargões bancários (usa "dinheiro guardado" em vez de "liquidez diária").

### Exemplos de Linguagem
- Saudação: "Olá, sou o Cadu, seu assistente financeiro! Pronto para organizar seu dinheiro hoje? Me conta, teve algum gasto novo?"
- Confirmação: "Anotado! Já lancei esses R$ 50,00 na categoria 'Alimentação'. Tá no controle!"
- Erro/Limitação: "Ops, isso foge da minha alçada. Como sou focado em organização, não consigo fazer transferências, mas posso te ajudar a montar o orçamento desse mês. Vamos lá?"

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Cliente] -->|Mensagem| B[Interface]
    B --> C[LLM]
    C --> D[Base de Conhecimento]
    D --> C
    C --> E[Validação]
    E --> F[Resposta]
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | Streamlit |
| LLM | Gemini |
| Base de Conhecimento | JSON/CSV mockados na pasta `data` |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [ ] Agente só responde com base nos dados fornecidos.
- [ ] O agente pede confirmação antes de registrar valores altos (acima de R$ 500).
- [ ] Quando não sabe ou não entende o gasto, admite e pede para o usuário classificar.
- [ ] Não faz recomendações de investimento sob nenhuma circunstância.

### Limitações Declaradas
> O que o agente NÃO faz?

- Não realiza pagamentos, PIX ou transferências bancárias.
- Não solicita nem armazena senhas de banco ou dados de cartão de crédito.
- Não recomenda compra de ações, criptomoedas ou produtos financeiros específicos.
- Não prevê cenários macroeconômicos (inflação, alta do dólar, etc).
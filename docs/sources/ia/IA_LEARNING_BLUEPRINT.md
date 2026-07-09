# Trilha IA - Blueprint de Aprendizagem

## Objetivo

Esta trilha organiza o estudo de Inteligencia Artificial aplicada em 12 decks progressivos no Anki.
O objetivo nao e decorar termos isolados, mas construir capacidade cumulativa para compreender, projetar, implementar e arquitetar sistemas modernos com IA.

## Principios Didaticos

- Progressao do simples para o complexo.
- Um conceito central por card.
- Preferencia por active recall e compreensao, nao por memorizacao literal.
- Reuso de conceitos entre decks apenas quando a perspectiva muda.
- Uso prioritario de fontes oficiais e curriculos tecnicos reconhecidos.

## Ordem da Trilha

### Onda A - Fundamentos e Modelos

1. IA::01 - Fundamentos
2. IA::02 - LLMs
3. IA::03 - Prompt Engineering
4. IA::04 - Context Engineering

### Onda B - Sistemas de Capacidade

5. IA::05 - Skills
6. IA::06 - MCP
7. IA::07 - RAG
8. IA::08 - Agentes
9. IA::09 - Multiagentes

### Onda C - Producao e Aplicacao

10. IA::10 - DevOps IA
11. IA::11 - Arquiteturas
12. IA::12 - Casos Reais

## Politica de Fontes

Ordem de prioridade para curadoria de conteudo:

1. OpenAI oficial
2. Anthropic oficial
3. Google AI oficial
4. Microsoft Learn AI
5. Hugging Face
6. DeepLearning.AI
7. Stanford CS224N
8. MIT e Berkeley
9. Papers cientificos relevantes
10. Artigos tecnicos oficiais

## Regras de Duplicidade

- Nao repetir um conceito no mesmo deck com formulacoes equivalentes.
- Um conceito pode reaparecer em deck posterior quando a lente muda.
- Exemplos validos de reuso: "token" em fundamentos, "tokenizacao" em LLMs, "custo por token" em DevOps IA.

## Regra de Saida por Deck

Cada deck deve entregar:

- cards em CSV no schema `card_id,front,back,deck,tags`
- relatorio pedagogico por deck
- bibliografia por deck
- justificativa da ordem dos cards

## Deck 01 - Escopo

O deck IA::01 - Fundamentos deve estabelecer o vocabulario minimo que sustenta toda a trilha:

- IA
- IA generativa
- Machine Learning
- Deep Learning
- redes neurais
- LLM
- token
- prompt
- contexto
- skill
- MCP
- agente
- limites de LLM
- diferenca entre treinamento e inferencia

## Observacao

Contexto longo, RAG, agentes e MCP devem ser ensinados como camadas complementares. Nenhum deles substitui sozinho o trabalho de arquitetura, curadoria de contexto, avaliacao e guardrails.
# E4.S1 - Modelo Logico de Integracao com Anki

## Objetivo

Definir a estrutura logica de decks, notas, tags, campos e midia para futura integracao com AnkiConnect.

## Pre-requisitos

- rastreabilidade de artefatos definida em E3;
- escopo do MVP aprovado em E5.S1;
- estrategia de integracao consolidada em ANKI_INTEGRATION_STRATEGY.

## Passos

### 1. Delimitar escopo do modelo

- modelo logico de nota;
- organizacao de decks e subdecks;
- estrategia de tags;
- associacao de audio e contexto;
- regras de identificacao unica.

### 2. Registrar fora do escopo

- chamadas reais para AnkiConnect;
- schema tecnico definitivo;
- automacao de importacao/exportacao.

### 3. Definir entidades logicas

### Deck

Representa o agrupamento principal de estudo.

Proposta inicial:
- deck raiz por modulo: Ingles;
- subdecks por habilidade: Listening;
- possibilidade futura de subdecks por nivel: A1, A2, B1, B2, C1.

Exemplo logico:
- Ingles::Listening::B1

### Nota

Representa a unidade primaria de conteudo sincronizavel.

Campos minimos sugeridos:
- source_id
- source_type
- title
- transcript_excerpt
- target_expression
- explanation_ptbr
- listening_context
- level
- accent
- tags_context
- audio_reference
- created_from_stage

### Card

Representa a projeção de estudo derivada da nota.

Diretriz:
- manter a logica centrada na nota;
- permitir multiplos cards por nota apenas quando houver justificativa pedagogica.

### Midia

Representa audio e, futuramente, imagens ou anexos.

Metadados minimos:
- media_id
- source_id
- media_type
- reference_path_or_url
- duration
- checksum_logico (futuro)

## Estrategia de tags

Tags devem ser compostas, previsiveis e reutilizaveis.

Categorias iniciais:
- modulo:ingles
- habilidade:listening
- nivel:B1
- origem:podcast
- sotaque:american
- fenomeno:connected_speech
- status:curated

## Regra de identificacao unica

Cada nota deve possuir um identificador logico unico baseado em:
- origem do conteudo;
- trecho ou item curado;
- fenomeno de estudo principal;
- nivel-alvo.

Objetivo:
- evitar duplicidade;
- permitir reconciliacao futura em sincronizacoes.

## Validacao

- todas as entidades logicas principais definidas;
- campos minimos da nota descritos;
- taxonomia inicial de tags documentada;
- regra de identificacao unica publicada e rastreavel.

## Troubleshooting

### Problema: inflacao de tags

Acao recomendada:

- revisar e consolidar categorias de tags antes da implementacao real.

### Problema: notas duplicadas

Acao recomendada:

- reforcar calculo de identificador unico e validacao previa no fluxo de sincronizacao.

### Problema: audio sem correspondencia

Acao recomendada:

- exigir metadados minimos de midia e bloqueio de envio em caso de referencia invalida.

## Riscos

- inflacao de tags sem taxonomia controlada;
- notas duplicadas para o mesmo trecho;
- audio sem correspondencia correta com a nota.

## Rastreabilidade

- Etapa/Subetapa: E4.S1
- Backlog: BLG-0010

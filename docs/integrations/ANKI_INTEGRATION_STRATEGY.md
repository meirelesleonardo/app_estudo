# Estrategia de Integracao Futura com Anki

## Objetivo

Documentar a arquitetura logica da integracao com Anki sem implementar ainda.

## Pre-requisitos

- modelo de dados e rastreabilidade definidos;
- curadoria validada;
- escopo do MVP consolidado.

## Passos

### 1. Definir escopo futuro

- criar cards automaticamente;
- atualizar cards existentes;
- organizar por decks e tags;
- associar audio e contexto;
- sincronizar revisoes.

### 2. Estruturar componentes logicos

1. Camada de mapeamento de conteudo
- transformar item de estudo em estrutura de nota.

2. Camada de normalizacao
- padronizar campos, tags e categorias.

3. Camada de integracao AnkiConnect
- operacoes de criar, atualizar e consultar.

4. Camada de controle de sincronizacao
- detectar divergencias e evitar duplicidade.

### 3. Definir estrategia de tags

- modulo:ingles
- habilidade:listening
- fenomeno:connected_speech
- nivel:B1
- origem:podcast

### 4. Definir metricas de acompanhamento

- taxa de duplicidade;
- taxa de atualizacao bem sucedida;
- tempo medio de sincronizacao;
- impacto na retencao de revisao.

## Validacao

- escopo e componentes logicos descritos de ponta a ponta;
- estrategia de tags publicada e consistente com E4;
- metricas futuras definidas;
- dependencias documentadas e verificaveis.

## Troubleshooting

### Risco: duplicidade de cards

Acao recomendada:

- reforcar regra de identificador logico unico em E4.S1;
- validar reconciliacao explicita em E4.S2.

### Risco: tags inconsistentes

Acao recomendada:

- centralizar taxonomia e revisar tags compostas antes da implementacao.

### Risco: midia sem vinculo correto

Acao recomendada:

- exigir metadados minimos de midia e estado pendente reprocessavel.

## Riscos

- duplicidade de cards;
- inconsistencia de tags;
- midia sem vinculo correto;
- divergencia entre fonte e card atualizado.

## Expansao em E4

- Modelo logico: [E4_LOGICAL_MODEL.md](E4_LOGICAL_MODEL.md)
- Fluxos de sincronizacao: [E4_SYNC_FLOWS.md](E4_SYNC_FLOWS.md)
- Tratamento de excecoes: [E4_EXCEPTION_HANDLING.md](E4_EXCEPTION_HANDLING.md)

## Rastreabilidade

- Etapa/Subetapa: E4 (visao estrategica)
- Backlog relacionado: BLG-0010, BLG-0015, BLG-0016

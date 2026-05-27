# Estrategia de Integracao Futura com Anki

## Objetivo

Documentar a arquitetura logica da integracao com Anki sem implementar ainda.

## Escopo futuro

- criar cards automaticamente;
- atualizar cards existentes;
- organizar por decks e tags;
- associar audio e contexto;
- sincronizar revisoes.

## Componentes logicos

1. Camada de mapeamento de conteudo
- transformar item de estudo em estrutura de nota.

2. Camada de normalizacao
- padronizar campos, tags e categorias.

3. Camada de integracao AnkiConnect
- operacoes de criar, atualizar e consultar.

4. Camada de controle de sincronizacao
- detectar divergencias e evitar duplicidade.

## Estrategia de tags (proposta)

- modulo:ingles
- habilidade:listening
- fenomeno:connected_speech
- nivel:B1
- origem:podcast

## Riscos

- duplicidade de cards;
- inconsistencia de tags;
- midia sem vinculo correto;
- divergencia entre fonte e card atualizado.

## Metricas futuras

- taxa de duplicidade;
- taxa de atualizacao bem sucedida;
- tempo medio de sincronizacao;
- impacto na retencao de revisao.

## Dependencias

- modelo de dados e rastreabilidade definidos;
- curadoria validada;
- escopo do MVP consolidado.

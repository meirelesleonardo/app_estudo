# Roadmap Incremental

## Visao Geral

Este roadmap organiza a evolucao do projeto em etapas controladas, com foco em qualidade documental, rastreabilidade e governanca antes de qualquer implementacao.

## Etapas

| Etapa | Nome | Status | Prioridade | Dependencias | Marco de Conclusao |
|---|---|---|---|---|---|
| E0 | Fundacao documental e governanca | Em andamento | Alta | Nenhuma | Repositorio com estrutura base e padroes definidos |
| E1 | Refinamento do modulo de ingles | Planejada | Alta | E0 | Escopo completo de listening e curadoria validado |
| E2 | Estrategia de fontes e avaliacao de conteudo | Planejada | Alta | E1 | Matriz de avaliacao e criterio de selecao prontos |
| E3 | Arquitetura de dados e rastreabilidade | Planejada | Alta | E0, E1, E2 | Modelo de entidades e trilha de decisao aprovados |
| E4 | Planejamento de integracao AnkiConnect | Planejada | Media | E3 | Contratos logicos e estrategia de tags revisados |
| E5 | Planejamento do MVP implementavel | Planejada | Alta | E1-E4 | Backlog de implementacao priorizado e refinado |
| E6 | Expansao para concursos e cybersec | Futuro | Media | E5 | Macroescopo do novo modulo consolidado |

## Backlog Macro por Etapa

### E0 - Fundacao documental e governanca
- Criar padroes de branch, commit, versao e changelog.
- Criar padroes de SPEC e ADR.
- Definir estrategia de continuidade entre chats.

### E1 - Refinamento do modulo de ingles
- Definir objetivos pedagogicos mensuraveis.
- Definir niveis de dificuldade e progressao.
- Definir tipos de midia aceitos por trilha.

### E2 - Fontes e avaliacao
- Curar e categorizar fontes por tipo e qualidade.
- Definir criterios de validacao das fontes.
- Definir rubric de avaliacao de listening.

### E3 - Dados e rastreabilidade
- Definir IDs de etapa, subetapa, item de backlog e decisao.
- Definir vinculo entre artefatos (roadmap, backlog, ADR, SPEC).
- Definir eventos de evolucao e historico.

### E4 - Integracao com Anki
- Definir arquitetura logica de decks, notas, tags e midia.
- Definir operacoes futuras com AnkiConnect.
- Definir estrategia de sincronizacao e tratamento de erros.

### E5 - MVP implementavel
- Definir escopo minimo implementavel.
- Quebrar backlog tecnico em SPECs pequenas.
- Definir criterio de pronto para implementacao.

### E6 - Expansao concursos/cybersec
- Definir trilhas de estudo por edital e disciplina.
- Definir simulados e revisao inteligente.
- Definir laboratorios praticos e banco de questoes.

## Proximos 30 dias (planejamento)

1. Consolidar E0 (sem codigo).
2. Finalizar refinamento de E1 e E2.
3. Publicar primeira versao de arquitetura de rastreabilidade (E3).

## Criterio de Avanco entre Etapas

Uma etapa so avanca quando:
- objetivo esta claro;
- escopo e nao escopo estao definidos;
- riscos e dependencias estao mapeados;
- backlog da etapa esta priorizado;
- criterio de conclusao esta explicito.

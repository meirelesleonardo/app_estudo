# Governanca do Projeto

## Objetivo

Padronizar como o projeto evolui, documenta decisoes e garante consistencia.

## Convencoes de nomenclatura

### Etapas e subetapas
- Etapa: E0, E1, E2...
- Subetapa: E1.S1, E1.S2...

### Backlog
- Item: BLG-0001, BLG-0002...

### Decisoes
- ADR: ADR-0001, ADR-0002...

### SPECs
- SPEC: SPEC-E1-S1-001

## Estrategia de branch

- main: historico estavel e documentacao validada.
- docs/<tema-curto>: alteracoes documentais.
- planning/<etapa>: refinamentos de etapa.
- spec/<id-spec>: preparacao de especificacoes aprovadas.

## Convencao de commits

Padrao sugerido:
- docs: atualiza curadoria de fontes E2
- roadmap: reprioriza backlog de E1
- governance: adiciona regra de branch
- trace: vincula BLG-0008 a E2.S2

## Versionamento

Durante fase documental:
- usar tags de marco, exemplo: v0.1-doc-foundation.

Quando houver codigo:
- adotar SemVer.

## Changelog

- manter registro em CHANGELOG.md;
- agrupar por Added, Changed, Deprecated, Removed, Fixed.

## Politica de decisoes arquiteturais

Toda decisao relevante deve:
- virar ADR;
- indicar contexto e alternativas;
- declarar impactos e trade-offs;
- apontar itens de backlog afetados.

## Definicao de pronto (documental)

Um item documental esta pronto quando:
- possui objetivo claro;
- possui criterio de conclusao;
- possui links para etapa e backlog;
- possui revisao minima de consistencia.

## Definicao de pronto para implementacao

Uma etapa so pode iniciar codigo se:
- refinamento e subetapas concluidos;
- SPEC aprovada;
- riscos principais mitigados;
- metricas de sucesso definidas.

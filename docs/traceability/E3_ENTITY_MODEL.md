# E3.S1 - Modelo de Entidades de Rastreabilidade

## Objetivo

Formalizar as entidades documentais do projeto, seus atributos minimos e suas relacoes logicas.

## Escopo

- entidades centrais do projeto;
- atributos obrigatorios por entidade;
- relacoes permitidas entre artefatos;
- base para auditoria e historico.

## Entidades principais

### 1. Etapa

Representa um bloco macro do roadmap.

Atributos minimos:
- id: E#
- nome
- status
- prioridade
- dependencias
- marco de conclusao

### 2. Subetapa

Representa uma decomposicao operacional de uma etapa.

Atributos minimos:
- id: E#.S#
- etapa-pai
- nome
- objetivo
- criterio de conclusao
- status

### 3. Item de backlog

Representa uma unidade priorizada de trabalho.

Atributos minimos:
- id: BLG-####
- titulo
- etapa/subetapa vinculada
- prioridade
- status
- criterio de conclusao

### 4. SPEC

Representa uma especificacao incremental pronta para orientar implementacao futura.

Atributos minimos:
- id: SPEC-<ETAPA>-<SUBETAPA>-<SEQ>
- etapa
- subetapa
- backlog relacionado
- status
- criterios de conclusao

### 5. ADR

Representa uma decisao arquitetural rastreavel.

Atributos minimos:
- id: ADR-####
- data
- status
- contexto
- problema
- decisao
- impacto na rastreabilidade

### 6. Marco

Representa um ponto de consolidacao do projeto.

Atributos minimos:
- id: M#
- nome
- data
- escopo do marco
- artefatos vinculados

### 7. Entrada de diario

Representa registro historico de evolucao da sessao.

Atributos minimos:
- data
- etapa/subetapa
- backlog trabalhado
- decisoes tomadas
- riscos identificados
- proximo passo

## Relacoes estruturais

- uma Etapa possui uma ou mais Subetapas;
- uma Subetapa pode possuir zero ou mais itens de backlog;
- um item de backlog pode originar zero ou mais SPECs;
- uma SPEC pode referenciar zero ou mais ADRs;
- um Marco consolida multiplos artefatos;
- uma entrada de diario pode referenciar backlog, etapa, subetapa e decisoes.

## Regras de integridade

1. Nenhuma Subetapa pode existir sem Etapa-pai valida.
2. Nenhum backlog pode existir sem vinculo a Etapa ou Subetapa.
3. Nenhuma SPEC pode existir sem backlog relacionado e gate pre-SPEC aprovado.
4. Nenhuma ADR pode existir sem impacto descrito em artefatos do projeto.
5. Nenhum marco pode ser fechado sem referencias para roadmap, backlog e changelog.

## Uso esperado em E3

Este modelo servira como base para:
- regras de vinculo entre artefatos;
- auditoria de mudancas;
- futuros templates e checklists automatizaveis.

## Rastreabilidade

- Etapa/Subetapa: E3.S1
- Dependencias: E0, E1, E2

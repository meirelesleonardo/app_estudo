# ADR Index

## Objetivo

Centralizar o catalogo de decisoes arquiteturais sem perder rastreabilidade com
etapas, backlog e SPECs.

## Convencao

- IDs sequenciais: ADR-0001, ADR-0002, ...
- Um arquivo por ADR em `docs/decisions/`.
- Toda ADR deve usar o template oficial.

## Estados de lifecycle

- Draft
- Refining
- Approved
- Deprecated

## Matriz de decisoes

| ID | Titulo | Status | Etapa/Subetapa | Backlog relacionado | SPEC relacionada | Data |
|---|---|---|---|---|---|---|
| ADR-0001 | Reservado para primeira decisao formal desta fase | Draft | E2.S4 | BLG-0023, BLG-0030 | N/A | 2026-05-27 |

## Regras minimas

1. Nao remover ADR antiga; usar estado Deprecated quando aplicavel.
2. Registrar impactos em backlog e rastreabilidade no mesmo ciclo da decisao.
3. Em caso de substituicao, referenciar explicitamente a ADR anterior.

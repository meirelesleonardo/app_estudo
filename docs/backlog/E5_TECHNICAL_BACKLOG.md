# E5.S2 - Backlog Tecnico Incremental (Candidatos a SPEC)

## Objetivo

Quebrar o MVP em incrementos pequenos, independentes e rastreaveis, sem gerar SPEC automaticamente.

## Regras de decomposicao

1. Cada incremento deve caber em uma SPEC pequena.
2. Cada incremento deve ter criterio de conclusao observavel.
3. Incrementos devem evitar acoplamento alto.
4. Ordem deve priorizar valor para validacao do fluxo minimo.

## Candidatos a SPEC (nao aprovadas ainda)

| Candidato | Objetivo | Dependencias | Criterio de conclusao |
|---|---|---|---|
| CSP-001 | Estruturar entidade de item de estudo curado | E3 | Campos minimos e regras de preenchimento definidos |
| CSP-002 | Aplicar matriz de avaliacao no item curado | CSP-001, E2 | Rubrica aplicada com score e classificacao final |
| CSP-003 | Mapear item para nota logica Anki | CSP-001, E4 | Mapeamento completo de campos e tags documentado |
| CSP-004 | Definir politica de deduplicacao logica | CSP-003, E4 | Regras de colisao e reconciliacao definidas |
| CSP-005 | Definir trilha de historico de alteracoes | E3 | Eventos e estados de auditoria por item definidos |
| CSP-006 | Definir lote piloto de validacao do MVP | CSP-001 a CSP-005 | Lote minimo, criterios de aceite e saida esperada definidos |

## Priorizacao sugerida

1. CSP-001
2. CSP-002
3. CSP-003
4. CSP-004
5. CSP-005
6. CSP-006

## Politica de passagem para SPEC

Um candidato so vira SPEC quando:
- passar no gate pre-SPEC;
- tiver backlog vinculado;
- tiver risco e dependencia explicitados;
- tiver criterio de conclusao objetivo.

## SPECs aprovadas

| Candidato | SPEC | Status | Evidencia |
|---|---|---|---|
| CSP-001 | SPEC-E5-S2-001 | Concluido | Entidade CuratedStudyItem + testes unitarios |
| CSP-002 | SPEC-E5-S2-002 | Concluido | Matriz de listening com score e classificacao + testes unitarios |
| CSP-003 | SPEC-E5-S2-003 | Concluido | Mapeamento para nota logica Anki + testes unitarios |
| CSP-004 | SPEC-E5-S2-004 | Concluido | Reconciliacao de duplicatas por source_id com dry-run/apply + testes unitarios |
| CSP-005 | SPEC-E5-S2-005 | Concluido | Trilha de historico por item em JSONL + consulta por filtro |
| CSP-006 | SPEC-E5-S2-006 | Concluido | Validacao automatizada de lote piloto com criterios de aceite do MVP |

## Rastreabilidade

- Etapa/Subetapa: E5.S2
- Backlog: BLG-0017

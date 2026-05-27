# Matriz de Rastreabilidade Unificada - E2.S4

## Objetivo

Consolidar em um unico ponto os vinculos entre subetapa, backlog, candidatos a SPEC,
artefatos, gates e evidencias esperadas para E2.S4.

## Escopo desta matriz

- E2.S4 - Ingestao e Processamento de Midia;
- backlog BLG-0023 a BLG-0029 e BLG-0032;
- candidatos CSP-E2-S4-001 a CSP-E2-S4-007;
- artefatos documentais e decisao ADR-0001.

## Matriz principal

| Subetapa | Backlog | Candidato a SPEC | Artefato principal | Dependencias | Gate alvo | Evidencia esperada |
|---|---|---|---|---|---|---|
| E2.S4 | BLG-0023 | CSP-E2-S4-001 | docs/english/E2_S4_INGESTAO_PROCESSAMENTO_MIDIA.md | BLG-0007, BLG-0008, BLG-0009 | Gate de definicao | Escopo, pipeline e limites formais publicados |
| E2.S4 | BLG-0024 | CSP-E2-S4-001, CSP-E2-S4-002 | docs/english/E2_S4_INGESTAO_PROCESSAMENTO_MIDIA.md | BLG-0023, BLG-0012 | Gate de rastreabilidade | Entidades e vinculos raw-curated definidos |
| E2.S4 | BLG-0025 | CSP-E2-S4-001 | docs/decisions/ADR-0001.md | BLG-0023 | Gate de risco | Contrato de origem YouTube com atributos obrigatorios |
| E2.S4 | BLG-0026 | CSP-E2-S4-003 | docs/english/E2_S4_INGESTAO_PROCESSAMENTO_MIDIA.md | BLG-0024, BLG-0009 | Gate de evidencia | Regras de normalizacao e versao de transformacao |
| E2.S4 | BLG-0027 | CSP-E2-S4-004, CSP-E2-S4-007 | docs/english/E2_S4_INGESTAO_PROCESSAMENTO_MIDIA.md | BLG-0026, E1.S2 | Gate de evidencia | Estrategia de chunking com granularidade formal |
| E2.S4 | BLG-0028 | CSP-E2-S4-005 | docs/english/E2_S4_INGESTAO_PROCESSAMENTO_MIDIA.md | BLG-0027, BLG-0013, BLG-0014 | Gate de coerencia | Persistencia de URLs, IDs, hashes, versoes e status |
| E2.S4 | BLG-0029 | CSP-E2-S4-006 | docs/english/E2_S4_INGESTAO_PROCESSAMENTO_MIDIA.md | BLG-0028, BLG-0014 | Gate de coerencia | Politicas de atualizacao, reconciliacao, invalidacao e reprocessamento |
| E2.S4 | BLG-0032 | CSP-E2-S4-001 a CSP-E2-S4-007 | docs/backlog/E2_S4_TECHNICAL_BACKLOG.md | BLG-0023 a BLG-0029 | Gate pre-SPEC | Backlog tecnico fechado com prioridades e criterios objetivos |

## Vinculos complementares de governanca

| Eixo | Artefato | Aplicacao em E2.S4 |
|---|---|---|
| Lifecycle | docs/governance/PROJECT_GOVERNANCE.md | Estados, gates e evidencias obrigatorias para transicao |
| Decisao arquitetural | docs/decisions/ADR-0001.md | Fonte oficial inicial de ingestao |
| Rastreabilidade base | docs/traceability/TRACEABILITY_MODEL.md | Regras de lineage e separacao raw-curated |
| Backlog operacional | docs/backlog/INITIAL_BACKLOG.md | IDs e criterios de conclusao dos itens BLG |
| Backlog tecnico | docs/backlog/E2_S4_TECHNICAL_BACKLOG.md | Decomposicao em candidatos a SPEC |

## Checklist de auditoria rapida

1. Todo BLG de E2.S4 tem criterio de conclusao observavel.
2. Todo CSP-E2-S4 possui dependencia e gate alvo declarado.
3. Toda decisao estrutural relevante de E2.S4 aponta para ADR.
4. Todo artefato de transcript preserva separacao raw-curated.
5. Toda transicao de lifecycle possui evidencia vinculada.

## Rastreabilidade

- Etapa/Subetapa: E2.S4
- Backlog: BLG-0023, BLG-0024, BLG-0025, BLG-0026, BLG-0027, BLG-0028, BLG-0029, BLG-0032
- ADR: ADR-0001
- Candidatos a SPEC: CSP-E2-S4-001, CSP-E2-S4-002, CSP-E2-S4-003, CSP-E2-S4-004, CSP-E2-S4-005, CSP-E2-S4-006, CSP-E2-S4-007

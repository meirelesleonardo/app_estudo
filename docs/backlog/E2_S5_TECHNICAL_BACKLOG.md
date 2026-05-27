# E2.S5 - Backlog Tecnico Incremental (Candidatos a SPEC)

## Objetivo

Quebrar E2.S5 em incrementos pequenos, independentes e rastreaveis,
sem iniciar implementacao tecnica neste ciclo.

## Candidatos a SPEC

| Candidato | Objetivo | Dependencias | Criterio de conclusao |
|---|---|---|---|
| CSP-E2-S5-001 | Definir contrato de KnowledgeSource, SourceProvider e TrustedSource | E2.S1, E3.S1 | Entidades e atributos obrigatorios de governanca publicados |
| CSP-E2-S5-002 | Definir politica SourceGovernancePolicy | CSP-E2-S5-001, E0 | Revisao, expiracao, versionamento, auditoria e rollback formalizados |
| CSP-E2-S5-003 | Definir matriz de uso por IA e bloqueios | CSP-E2-S5-002, E6.S2 | Regras AUTO/HUMAN_REVIEW/PROHIBITED documentadas |
| CSP-E2-S5-004 | Definir governanca YouTube para curadoria audiovisual | ADR-0001, E2.S3, CSP-E2-S5-002 | Criterios de legenda, naturalidade, densidade pedagogica, ruido, velocidade e sotaque formalizados |
| CSP-E2-S5-005 | Definir pipeline Trusted Source -> Sync Pipeline | E2.S4, CSP-E2-S5-003 | Fluxo ponta a ponta com gates e evidencias publicado |

## Priorizacao sugerida

1. CSP-E2-S5-001
2. CSP-E2-S5-002
3. CSP-E2-S5-003
4. CSP-E2-S5-004
5. CSP-E2-S5-005

## Politica de passagem para SPEC

Um candidato so vira SPEC quando:
- passar no gate pre-SPEC;
- tiver backlog vinculado;
- tiver risco e dependencia explicitados;
- tiver criterio de conclusao observavel;
- tiver impacto declarado em rastreabilidade e uso por IA.

## Rastreabilidade

- Etapa/Subetapa: E2.S5
- Backlog: BLG-0033, BLG-0034, BLG-0035, BLG-0036, BLG-0037, BLG-0038

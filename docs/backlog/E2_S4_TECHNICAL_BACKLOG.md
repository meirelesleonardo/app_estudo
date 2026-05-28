# E2.S4 - Backlog Tecnico Incremental (Candidatos a SPEC)

## Objetivo

Quebrar a subetapa E2.S4 em incrementos pequenos, independentes e rastreaveis,
sem iniciar implementacao tecnica neste ciclo.

## Regras de decomposicao

1. Cada incremento deve caber em uma SPEC pequena.
2. Cada incremento deve ter criterio de conclusao observavel.
3. Incrementos devem minimizar acoplamento entre ingestao, texto e sincronizacao.
4. Ordem deve priorizar rastreabilidade da origem e qualidade do dado textual.

## Candidatos a SPEC (nao aprovadas ainda)

| Candidato | Objetivo | Dependencias | Criterio de conclusao |
|---|---|---|---|
| CSP-E2-S4-001 | Definir contrato de SourceMedia e SourceMetadata | E2.S1, E3.S1 | Entidades de origem com campos obrigatorios e regras de identificacao univoca documentadas |
| CSP-E2-S4-002 | Definir contrato de RawTranscript e CuratedTranscript | CSP-E2-S4-001, E2.S3, E3.S1 | Separacao raw-curated e lineage documentados com atributos, status e versoes |
| CSP-E2-S4-003 | Definir pipeline de normalizacao textual | CSP-E2-S4-002, E2.S3 | Regras de normalizacao, flags de transformacao e saida versionada documentadas |
| CSP-E2-S4-004 | Definir estrategia de segmentacao pedagogica | CSP-E2-S4-003, E1.S2 | Granularidade video-segmento-frase-unidade pedagogica e limites operacionais definidos |
| CSP-E2-S4-005 | Definir persistencia de metadados e hashes | CSP-E2-S4-001 a CSP-E2-S4-004, E3.S3 | Estrategia de armazenamento e trilha de auditoria por artefato definida |
| CSP-E2-S4-006 | Definir politica de versionamento e reprocessamento | CSP-E2-S4-005, E3.S3 | Regras de atualizacao, reconciliacao, invalidacao e reprocessamento publicadas |
| CSP-E2-S4-007 | Definir gate de qualidade para entrada no fluxo E4 | CSP-E2-S4-004, CSP-E2-S4-006, E4.S1 | Checklist minimo para transformar segmento curado em item apto ao mapeamento logico documentado |

## Priorizacao sugerida

1. CSP-E2-S4-001
2. CSP-E2-S4-002
3. CSP-E2-S4-003
4. CSP-E2-S4-004
5. CSP-E2-S4-005
6. CSP-E2-S4-006
7. CSP-E2-S4-007

## Politica de passagem para SPEC

Um candidato so vira SPEC quando:
- passar no gate pre-SPEC;
- tiver backlog vinculado;
- tiver risco e dependencia explicitados;
- tiver criterio de conclusao objetivo;
- tiver impacto declarado em rastreabilidade e auditoria.

## Rastreabilidade

- Etapa/Subetapa: E2.S4
- Backlog: BLG-0032
- Dependencias: BLG-0023, BLG-0024, BLG-0025, BLG-0026, BLG-0027, BLG-0028, BLG-0029

## SPECs criadas neste ciclo (aguardando gate pre-SPEC)

| Candidato | SPEC | Status | Evidencia |
|---|---|---|---|
| CSP-E2-S4-001 | SPEC-E2-S4-001 | Concluido | Entidades SourceMedia/SourceMetadata implementadas + testes unitarios |
| CSP-E2-S4-002 | SPEC-E2-S4-002 | Proposta pronta para gate pre-SPEC | Contrato RawTranscript/CuratedTranscript com lineage documentado |
| CSP-E2-S4-003 | SPEC-E2-S4-003 | Proposta pronta para gate pre-SPEC | Pipeline de normalizacao textual versionada documentado |

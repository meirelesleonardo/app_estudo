# Matriz de Rastreabilidade Unificada - E2.S5, E6.S4 e E6.S5

## Objetivo

Consolidar vinculos entre backlog, artefatos, candidatos a SPEC, gates e evidencias
para a expansao de governanca de fontes e base de conhecimento confiavel.

## Escopo

- E2.S5 - Governanca e Curadoria de Fontes;
- E6.S4 - Motor Inteligente de Questoes;
- E6.S5 - Taxonomia e Ontologia de Cyber Seguranca.

## Matriz principal

| Subetapa | Backlog | Candidato a SPEC | Artefato principal | Dependencias | Gate alvo | Evidencia esperada |
|---|---|---|---|---|---|---|
| E2.S5 | BLG-0033 | CSP-E2-S5-001 | docs/sources/governance/SOURCE_GOVERNANCE_POLICY.md | E2.S1, E3.S1 | Gate de definicao | Classificacao, confiabilidade e uso por IA formalizados |
| E2.S5 | BLG-0034 | CSP-E2-S5-002 | docs/sources/README.md | BLG-0033 | Gate de rastreabilidade | Estrutura de catalogo por dominio com atributos obrigatorios |
| E2.S5 | BLG-0035 | CSP-E2-S5-003 | docs/sources/governance/SOURCE_GOVERNANCE_POLICY.md | BLG-0033, E0 | Gate de risco | Politicas de revisao, expiracao, versionamento e auditoria publicadas |
| E2.S5 | BLG-0036 | CSP-E2-S5-004 | docs/sources/governance/SOURCE_GOVERNANCE_POLICY.md | BLG-0035, E6.S2 | Gate de evidencia | Matriz de autorizacao por IA publicada |
| E2.S5 | BLG-0037 | CSP-E2-S5-005 | docs/sources/governance/KNOWLEDGE_PIPELINE_TRUSTED.md | E2.S4, BLG-0036 | Gate de coerencia | Fluxo Trusted Source -> Sync Pipeline com gates de qualidade |
| E2.S5 | BLG-0038 | CSP-E2-S5-006 | docs/sources/operational/YOUTUBE_CURATION_POLICY.md | ADR-0001, E2.S3 | Gate de risco | Curadoria YouTube com metricas de qualidade e bloqueio de automacao indevida |
| E6.S1 | BLG-0039 | CSP-E6-S1-004 | docs/sources/frameworks/CYBERSEC_OFFICIAL_FRAMEWORKS.md | BLG-0020, E2.S5 | Gate de definicao | Catalogo de fontes oficiais prioritarias publicado |
| E6.S1 | BLG-0040 | CSP-E6-S1-005 | docs/sources/concursos/COMPETITION_SOURCE_POLICY.md | BLG-0020, E6.S2 | Gate de rastreabilidade | Estrutura por banca com recorrencia e estilo textual |
| E6.S4 | BLG-0041 | CSP-E6-S4-001 | docs/cybersec/E6_S4_INTELLIGENT_QUESTION_ENGINE.md | E6.S2, E6.S3, E2.S5 | Gate pre-SPEC | Contrato do motor de questoes adaptativas definido |
| E6.S5 | BLG-0042 | CSP-E6-S5-001 | docs/cybersec/E6_S5_CYBERSEC_TAXONOMY_ONTOLOGY.md | E6.S1, E2.S5 | Gate de evidencia | Taxonomia e ontologia com relacoes semanticas publicadas |
| E6.S5 | BLG-0043 | CSP-E6-S5-002 | docs/sources/governance/KNOWLEDGE_ENTITY_MODEL.md | BLG-0041, BLG-0042 | Gate de coerencia | Entidades de conhecimento para RAG pedagogico com riscos e relacoes |
| E3.S2 | BLG-0044 | CSP-E3-S2-004 | docs/traceability/E2_S5_E6_TRACEABILITY_MATRIX.md | BLG-0033 a BLG-0043 | Gate de evidencia | Matriz unificada com vinculos completos e evidencias |

## Checklist rapido

1. Nenhuma automacao de IA usa fonte sem confiabilidade declarada.
2. Toda fonte trusted tem revisao e expiracao preenchidas.
3. Toda decisao relevante aponta para ADR, backlog e artefato.
4. Toda unidade de conhecimento tem lineage para fonte de origem.
5. Conteudo experimental segue separado do fluxo oficial.

## Rastreabilidade

- Etapa/Subetapa: E2.S5, E6.S4, E6.S5
- Backlog: BLG-0033 a BLG-0044
- ADR: ADR-0001

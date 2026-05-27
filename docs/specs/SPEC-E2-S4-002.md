# SPEC-E2-S4-002 - Contrato de RawTranscript e CuratedTranscript

## Identificacao

- ID: SPEC-E2-S4-002
- Etapa: E2
- Subetapa: E2.S4
- Backlog relacionado: BLG-0032 (CSP-E2-S4-002), BLG-0024, BLG-0028, BLG-0031
- Status: Proposta pronta para gate pre-SPEC

## 1. Contexto

Com o contrato de origem definido em SPEC-E2-S4-001, o segundo incremento deve
formalizar a separacao entre conteudo bruto e curado para preservar auditabilidade,
permitir rollback documental e sustentar reprocessamento seguro.

## 2. Objetivo

Definir contrato de RawTranscript e CuratedTranscript com vinculos de lineage,
status de curadoria, versionamento e evidencias minimas de rastreabilidade.

## 3. Escopo

- definir atributos obrigatorios de RawTranscript;
- definir atributos obrigatorios de CuratedTranscript;
- definir vinculos obrigatorios entre SourceMedia, RawTranscript e CuratedTranscript;
- definir estados de curadoria para transcript;
- definir evidencias minimas de lineage para auditoria.

## 4. Fora do escopo

- algoritmo de normalizacao textual;
- segmentacao pedagogica;
- extracao de audio e cortes por timestamp;
- sincronizacao com Anki.

## 5. Dependencias

- SPEC-E2-S4-001;
- E2.S3 (validacao de legenda/transcricao);
- E3.S2 (regras de vinculo entre artefatos);
- E3.S3 (auditoria e historico).

## 6. Riscos

- perda de lineage por mistura de raw e curated em uma unica estrutura;
- ausencia de status claro dificultando governanca de curadoria;
- versoes sem hash impossibilitando deteccao de divergencia.

## 7. Metricas de sucesso

- separacao raw/curated documentada sem ambiguidades;
- 100% dos campos de lineage obrigatorios definidos;
- estados de transcript curado publicados com criterios de transicao;
- vinculo com trilha de auditoria formalizado.

## 8. Criterios de conclusao

- contrato de RawTranscript publicado com atributos e regras;
- contrato de CuratedTranscript publicado com atributos e regras;
- matriz de lineage minima publicada (source -> raw -> curated);
- checklist de auditoria de transcript publicado.

## 9. Entregaveis

- especificacao de RawTranscript;
- especificacao de CuratedTranscript;
- matriz de lineage para transcricao;
- checklist de auditoria de transicao raw-curated.

## 10. Plano incremental

1. Definir contrato de RawTranscript e identificadores obrigatorios.
2. Definir contrato de CuratedTranscript e estados de curadoria.
3. Definir matriz de lineage e evidencias minimas por transicao.
4. Consolidar checklist de auditoria para gate de qualidade.

## 11. Rastreabilidade

- Roadmap: E2.S4
- Backlog: BLG-0032 / CSP-E2-S4-002, BLG-0024, BLG-0028, BLG-0031
- ADR relacionada: ADR-0001
- Changelog: secao Unreleased

## 12. Proximos passos

- Evoluir para SPEC-E2-S4-003 para normalizacao textual versionada.

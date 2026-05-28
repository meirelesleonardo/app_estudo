# SPEC-E2-S4-007 - Gate de Qualidade para Entrada no Fluxo E4

## Identificacao

- ID: SPEC-E2-S4-007
- Etapa: E2
- Subetapa: E2.S4
- Backlog relacionado: BLG-0032 (CSP-E2-S4-007), BLG-0027, BLG-0031
- Status: Concluida (implementacao inicial)

## 1. Contexto

A trilha E2.S4 ja possui contratos de origem/transcript, normalizacao, segmentacao,
persistencia SQLite e politica de versionamento. O incremento final e estabelecer
gate de qualidade antes de entrada no fluxo E4.

## 2. Objetivo

Implementar checklist executavel para decidir aprovacao/reprovacao de artefatos
curados para entrada no fluxo E4 e preparar ingestao inicial de YouTube.

## 3. Escopo

- implementar gate de qualidade com checklist explicito;
- avaliar consistencia entre metadados, transcript curado e segmentos;
- bloquear entrada quando politica de versionamento indicar invalidate/reprocess;
- disponibilizar adaptador inicial de ingestao YouTube com persistencia SQLite.

## 4. Fora do escopo

- download de audio do YouTube;
- ingestao em lote multi-video;
- resiliencia de rede para fontes externas em producao;
- sincronizacao automatica com Anki em runtime.

## 5. Dependencias

- SPEC-E2-S4-004;
- SPEC-E2-S4-005;
- SPEC-E2-S4-006;
- E4.S1 (modelo logico de entrada no fluxo Anki).

## 6. Riscos

- gate permissivo demais liberar artefatos com baixa confiabilidade;
- gate restritivo demais bloquear progresso operacional;
- ingestao inicial sem checklist aumentar retrabalho no fluxo E4.

## 7. Metricas de sucesso

- checklist de gate com cobertura de testes para aprovar/reprovar;
- decisao de gate com motivos rastreaveis;
- adaptador YouTube persistindo artefatos no SQLite de ponta a ponta;
- suite de testes global sem regressao.

## 8. Criterios de conclusao

- gate de qualidade implementado e testado;
- adaptador YouTube implementado e testado;
- export dos novos componentes no pacote de integracoes;
- backlog e changelog atualizados com evidencias.

## 9. Entregaveis

- modulo `media_quality_gate`;
- modulo `youtube_ingestion`;
- testes unitarios dos dois modulos;
- registros de rastreabilidade da conclusao.

## 10. Plano incremental

1. Implementar checklist de qualidade para entrada em E4.
2. Integrar criterio de bloqueio por decisao de versionamento.
3. Implementar adaptador YouTube para ingestao inicial em SQLite.
4. Validar com testes focais e suite completa.

## 11. Rastreabilidade

- Roadmap: E2.S4
- Backlog: BLG-0032 / CSP-E2-S4-007, BLG-0027, BLG-0031
- ADR relacionada: ADR-0001
- Changelog: secao Unreleased

## 12. Proximos passos

- Executar smoke test com URL real do primeiro video YouTube para lote piloto.

## Evidencias de implementacao

- Gate `evaluate_e4_quality_gate` implementado com checklist de aprovacao/reprovacao.
- Adaptador `ingest_first_youtube_video` implementado para persistir origem, transcript e segmentos em SQLite.
- Testes unitarios adicionados para gate de qualidade e ingestao YouTube.
- Suite completa validada sem regressao.

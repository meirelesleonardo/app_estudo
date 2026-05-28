# SPEC-E2-S4-006 - Politica de Versionamento e Reprocessamento

## Identificacao

- ID: SPEC-E2-S4-006
- Etapa: E2
- Subetapa: E2.S4
- Backlog relacionado: BLG-0032 (CSP-E2-S4-006), BLG-0029, BLG-0031
- Status: Concluida (implementacao inicial)

## 1. Contexto

Com persistencia SQLite de artefatos e trilha de auditoria implementadas, a etapa
seguinte e definir um motor de decisao para versionamento e reprocessamento de
artefatos, garantindo regras explicitas e reproduziveis de transicao.

## 2. Objetivo

Implementar politica executavel para decidir entre update, substitute, reconcile,
invalidate e reprocess, com rastreabilidade de motivo da decisao.

## 3. Escopo

- definir estrutura de snapshot de artefato para comparacao;
- implementar decisor de acao de versionamento;
- cobrir cenarios de update/substitute/reconcile/invalidate/reprocess;
- expor API de versionamento no pacote de integracoes.

## 4. Fora do escopo

- orquestrador automatico de fila de reprocessamento;
- monitoramento de longo prazo de drift;
- rollback automatico entre versoes em lote;
- extracao direta de midia do YouTube.

## 5. Dependencias

- SPEC-E2-S4-005;
- E3.S3 (auditoria e historico);
- E2.S3 (validacao de confiabilidade textual).

## 6. Riscos

- regra de decisao ambigua gerar inconsistencias em reprocessamento;
- condicoes de invalidacao mal calibradas descartarem artefatos validos;
- ausencia de motivo explicito dificultar auditoria de transicao.

## 7. Metricas de sucesso

- 100% das acoes previstas na politica com cobertura de teste;
- retorno de decisao com acao + motivo explicito;
- validacao de pre-condicoes de comparacao por artefato;
- integracao do decisor no pacote de integracoes.

## 8. Criterios de conclusao

- engine de versionamento implementada;
- testes unitarios cobrindo cenarios validos e invalidos aprovados;
- rastreabilidade atualizada para CSP-E2-S4-006;
- changelog e diario atualizados com evidencias.

## 9. Entregaveis

- modulo `media_versioning`;
- estruturas `ArtifactSnapshot` e `VersionDecision`;
- funcao `decide_version_action`;
- testes unitarios de politica de transicao.

## 10. Plano incremental

1. Definir contrato de snapshots para comparacao.
2. Implementar regras de decisao por prioridade.
3. Cobrir regras por testes unitarios.
4. Expor API no pacote de integracoes.

## 11. Rastreabilidade

- Roadmap: E2.S4
- Backlog: BLG-0032 / CSP-E2-S4-006, BLG-0029, BLG-0031
- ADR relacionada: ADR-0001
- Changelog: secao Unreleased

## 12. Proximos passos

- Evoluir para SPEC-E2-S4-007 (gate de qualidade para entrada no fluxo E4).

## Evidencias de implementacao

- Engine `decide_version_action` implementada com suporte a update, substitute, reconcile, invalidate e reprocess.
- Estruturas `ArtifactSnapshot` e `VersionDecision` implementadas para rastreabilidade de decisao.
- Testes unitarios cobrindo cenarios de transicao e validacao de comparacao aprovados.
- API de versionamento exportada no pacote `app_estudo.integrations`.

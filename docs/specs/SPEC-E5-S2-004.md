# SPEC-E5-S2-004 - Duplicacao Logica e Reconciliacao

## Identificacao

- ID: SPEC-E5-S2-004
- Etapa: E5
- Subetapa: E5.S2
- Backlog relacionado: BLG-0017 (CSP-004)
- Status: Aprovada para implementacao incremental

## 1. Contexto

Com o fluxo create/update e a migracao de deck legada concluida, o proximo incremento e tratar conflitos de duplicidade de forma controlada, rastreavel e reprocessavel.

## 2. Objetivo

Implementar politica de deduplicacao logica por source_id com reconciliacao em modo dry-run e modo apply.

## 3. Escopo

- detectar grupos de notas com source_id duplicado;
- escolher nota canonica por estrategia declarada;
- consolidar tags na nota canonica;
- remover notas duplicadas quando apply estiver habilitado;
- relatar resultado com estados e contagens.

## 4. Fora do escopo

- deduplicacao sem source_id;
- reconciliacao sem criterio explicito;
- alteracoes massivas sem dry-run;
- heuristicas sem evidencia minima.

## 5. Dependencias

- CSP-001 a CSP-003 concluidos;
- cliente base de AnkiConnect (SPEC-E4-S2-001);
- regras de estados de E4.S2/E4.S3.

## 6. Riscos

- perda indevida de dados ao apagar duplicatas sem consolidacao;
- escolha canonica inadequada em casos ambiguos;
- conflito recorrente sem observabilidade de resultado.

## 7. Metricas de sucesso

- 100% dos grupos duplicados identificados no dry-run;
- 100% dos grupos reconciliados com estrategia declarada em apply;
- 0 falhas silenciosas no relatorio de reconciliacao.

## 8. Criterios de conclusao

- modulo de reconciliacao implementado;
- script CLI de dry-run/apply disponivel;
- testes unitarios cobrindo plano e execucao de reconciliacao.

## 9. Entregaveis

- modulo de reconciliacao de duplicatas;
- integracao com cliente AnkiConnect;
- script operacional de reconciliacao;
- documentacao e rastreabilidade atualizadas.

## 10. Plano incremental

1. Implementar modelo de plano de reconciliacao.
2. Implementar detector de grupos por source_id.
3. Implementar execucao dry-run e apply com consolidacao de tags.
4. Cobrir com testes e registrar evidencias.

## 11. Rastreabilidade

- Roadmap: E5
- Backlog: BLG-0017 / CSP-004
- ADR relacionada: N/A neste incremento
- Changelog: secao Unreleased

## 12. Proximos passos

- Evoluir CSP-005 (trilha de historico de alteracoes por item).

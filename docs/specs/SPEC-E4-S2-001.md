# SPEC-E4-S2-001 - Cliente Base de Integracao com AnkiConnect

## Identificacao

- ID: SPEC-E4-S2-001
- Etapa: E4
- Subetapa: E4.S2
- Backlog relacionado: BLG-0015
- Status: Aprovada para implementacao incremental

## 1. Contexto

A camada logica de mapeamento para nota Anki ja foi implementada. O proximo passo e habilitar uma camada tecnica de comunicacao com AnkiConnect para criar e atualizar notas com tratamento explicito de estados e falhas.

## 2. Objetivo

Implementar cliente base de AnkiConnect com sincronizacao minima (create/update), mantendo rastreabilidade dos estados de sincronizacao.

## 3. Escopo

- executar chamadas action/version 6 ao endpoint local;
- buscar notas por source_id;
- criar nota quando nao existir;
- atualizar campos e tags quando nota existir;
- classificar resultado em estados logicos (synced, updated, conflict, pending, blocked).

## 4. Fora do escopo

- politica completa de deduplicacao e reconciliacao (CSP-004);
- orquestracao de lotes grandes;
- telemetria e retry automatico em producao;
- testes integrados com Anki real no CI.

## 5. Dependencias

- E4.S1 (modelo logico de nota);
- E4.S2 (fluxos de sincronizacao);
- E4.S3 (tratamento de excecoes);
- CSP-003 (payload logico de nota pronto).

## 6. Riscos

- erro remoto do AnkiConnect bloquear sync;
- inconsistencia de campos obrigatorios;
- conflito por duplicidade de notas.

## 7. Metricas de sucesso

- 100% dos fluxos create/update testados por mocks;
- estados de retorno coerentes com E4.S2;
- erros de conectividade mapeados para estado pending.

## 8. Criterios de conclusao

- cliente base implementado com API de sync;
- cobertura de testes para create/update/conflict/pending/blocked;
- validacao de payload minimo obrigatorio antes do envio.

## 9. Entregaveis

- modulo ankiconnect_client;
- testes unitarios do cliente;
- atualizacao de guia de ambiente com ponto de verificacao tecnica.

## 10. Plano incremental

1. Implementar camada de request/response e excecoes.
2. Implementar sync create/update baseado em source_id.
3. Mapear estados logicos de sucesso e falha.
4. Cobrir fluxos com testes via mock.

## 11. Rastreabilidade

- Roadmap: E4
- Backlog: BLG-0015
- ADR relacionada: N/A neste incremento
- Changelog: secao Unreleased

## 12. Proximos passos

- Implementar politica de deduplicacao e reconciliacao (CSP-004).
- Conectar com Anki real para smoke test local.

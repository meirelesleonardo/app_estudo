# SPEC-E5-S2-005 - Trilha de Historico de Alteracoes por Item

## Identificacao

- ID: SPEC-E5-S2-005
- Etapa: E5
- Subetapa: E5.S2
- Backlog relacionado: BLG-0017 (CSP-005)
- Status: Aprovada para implementacao incremental

## 1. Contexto

Com sincronizacao, deduplicacao e reconciliacao implementadas, falta registrar historico por item para auditoria operacional, investigacao de falhas e reprocessamento orientado por evidencia.

## 2. Objetivo

Implementar trilha de eventos por item com persistencia local em formato JSONL e consulta por item/evento.

## 3. Escopo

- registrar eventos de sync e reconciliacao;
- armazenar data, item, tipo de mudanca, motivo e impacto tecnico;
- permitir consulta filtrada por item ou tipo de evento;
- manter formato simples e rastreavel para auditoria.

## 4. Fora do escopo

- armazenamento em banco externo;
- agregacao analitica avancada;
- dashboard visual;
- telemetria distribuida.

## 5. Dependencias

- E3.S3 (auditoria e historico);
- cliente de sincronizacao Anki (SPEC-E4-S2-001);
- politica de reconciliacao (SPEC-E5-S2-004).

## 6. Riscos

- excesso de eventos sem filtro util;
- historico local sem politica de retencao futura;
- inconsistencias sem padrao de evento.

## 7. Metricas de sucesso

- 100% das operacoes de sync/reconciliacao geram evento auditavel;
- consultas por item retornam trilha completa do ciclo;
- nenhum evento critico sem timestamp e estado.

## 8. Criterios de conclusao

- store JSONL implementado e testado;
- cliente integrado ao registro automatico de eventos;
- script de consulta operacional disponivel.

## 9. Entregaveis

- modulo item_history;
- integracao no cliente AnkiConnect;
- script de leitura de historico;
- testes unitarios da trilha de eventos.

## 10. Plano incremental

1. Definir schema de evento e store JSONL.
2. Integrar eventos nos fluxos de sync/reconciliacao.
3. Implementar script de consulta por filtros.
4. Validar com testes e atualizar rastreabilidade.

## 11. Rastreabilidade

- Roadmap: E5
- Backlog: BLG-0017 / CSP-005
- ADR relacionada: N/A neste incremento
- Changelog: secao Unreleased

## 12. Proximos passos

- Executar CSP-006 com lote piloto e metricas de aceite do MVP.

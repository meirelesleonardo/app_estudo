# E5.S3 - Criterio de Pronto para Implementacao

## Objetivo

Definir a condicao formal para iniciar implementacao sem comprometer governanca e rastreabilidade.

## Definicao de pronto para implementacao

Uma frente esta pronta para implementacao quando atende simultaneamente:

1. Refinamento concluido
- etapa e subetapa fechadas documentalmente.

2. Gate pre-SPEC aprovado
- checklist obrigatorio completo com evidencias.

3. Backlog priorizado e rastreavel
- item com ID, criterio de conclusao, dependencias e status coerentes.

4. Riscos mapeados
- riscos principais com estrategia de mitigacao definida.

5. Entregavel incremental claro
- escopo pequeno, independente e verificavel.

## Itens de bloqueio (nao iniciar)

- ausencia de vinculo entre roadmap e backlog;
- escopo amplo sem recorte incremental;
- falta de criterio de sucesso mensuravel;
- decisao estrutural sem ADR quando necessaria.

## Checklist de autorizacao

- [x] Etapa/Subetapa concluida
- [x] Backlog vinculado e priorizado
- [x] Gate pre-SPEC aprovado
- [x] Criterio de conclusao definido
- [x] Risco e dependencia mapeados
- [x] Registro em diario e changelog quando aplicavel

## Evidencias minimas

- links para artefatos da etapa;
- referencia do backlog;
- status atualizado no roadmap;
- registro de sessao no diario.

## Fechamento do Gate Final do MVP (CSP-001 a CSP-006)

### Resultado consolidado

- Status final do gate: aprovado
- Deck validado: Ingles::Listening::B1
- Data de consolidacao: 2026-05-27

### Evidencias operacionais

- Lote piloto validado com status approved.
- Metricas finais do lote:
	- total_notes: 45
	- min_items_target: 20
	- traceability_pct: 100.0
	- duplicate_rate_pct: 0.0
	- classification_pct: 100.0
- Trilha de auditoria confirma evolucao de needs_review para approved em pilot_validation.

### Matriz de evidencias por incremento

| Incremento | SPEC | Evidencia principal |
|---|---|---|
| CSP-001 | SPEC-E5-S2-001 | Entidade CuratedStudyItem + testes unitarios |
| CSP-002 | SPEC-E5-S2-002 | Matriz de listening com score e classificacao + testes unitarios |
| CSP-003 | SPEC-E5-S2-003 | Mapeamento para nota logica Anki + testes unitarios |
| CSP-004 | SPEC-E5-S2-004 | Reconciliacao dry-run/apply por source_id + testes unitarios |
| CSP-005 | SPEC-E5-S2-005 | Trilha JSONL de historico + script de consulta |
| CSP-006 | SPEC-E5-S2-006 | Validacao automatizada do lote piloto + backfill de campos criticos + status approved |

### Decisao

Gate final do MVP aprovado para operacao controlada com curadoria continua dos placeholders de audio_reference.

## Rastreabilidade

- Etapa/Subetapa: E5.S3
- Backlog: BLG-0018

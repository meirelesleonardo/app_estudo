# SPEC-E5-S2-006 - Lote Piloto e Criterios de Aceite do MVP

## Identificacao

- ID: SPEC-E5-S2-006
- Etapa: E5
- Subetapa: E5.S2
- Backlog relacionado: BLG-0017 (CSP-006)
- Status: Aprovada para implementacao incremental

## 1. Contexto

Com CSP-001 a CSP-005 concluidos, o proximo incremento e validar um lote piloto real com criterios objetivos para declarar o MVP apto para operacao controlada.

## 2. Objetivo

Definir e executar validacao automatizada de lote piloto, com metricas de aceite do MVP e resultado auditavel.

## 3. Escopo

- definir criterios objetivos de aceite do lote piloto;
- validar cobertura de rastreabilidade por item;
- validar taxa de duplicidade logica no lote;
- validar cobertura de classificacao pedagogica;
- emitir relatorio operacional com status aprovado ou needs_review.

## 4. Fora do escopo

- liberacao de producao em larga escala;
- otimizacao de desempenho para alto volume;
- dashboard grafico;
- reprocessamento automatico de correcoes.

## 5. Dependencias

- CSP-001 a CSP-005 concluidos;
- cliente AnkiConnect operacional (SPEC-E4-S2-001);
- trilha de historico local (SPEC-E5-S2-005).

## 6. Riscos

- lote menor que o minimo estatistico para validacao;
- falso positivo de aceite por campos preenchidos sem qualidade semantica;
- criterios sem threshold explicito dificultando decisao go/no-go.

## 7. Metricas de sucesso

- lote com pelo menos 20 notas avaliadas;
- rastreabilidade por item >= 95%;
- duplicidade logica <= 2%;
- classificacao pedagogica preenchida em 100% das notas do lote.

## 8. Criterios de conclusao

- modulo de validacao de lote piloto implementado;
- comando CLI para executar validacao do lote;
- resultado registrado com status aprovado ou needs_review;
- testes unitarios cobrindo cenarios aprovado e needs_review.

## 9. Entregaveis

- modulo pilot_validation;
- metodo no cliente Anki para avaliar lote piloto;
- script validate_mvp_pilot.py;
- testes unitarios do validador.

## 10. Plano incremental

1. Definir metricas e thresholds do lote piloto.
2. Implementar validador baseado em notesInfo.
3. Integrar no cliente Anki com registro em historico.
4. Criar script CLI e validar em execucao real.

## 11. Rastreabilidade

- Roadmap: E5
- Backlog: BLG-0017 / CSP-006
- ADR relacionada: N/A neste incremento
- Changelog: secao Unreleased

## 12. Proximos passos

- Consolidar evidencias do lote e iniciar gate de aceite final do MVP.

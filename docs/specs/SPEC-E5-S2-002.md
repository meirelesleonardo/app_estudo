# SPEC-E5-S2-002 - Matriz de Avaliacao de Listening

## Identificacao

- ID: SPEC-E5-S2-002
- Etapa: E5
- Subetapa: E5.S2
- Backlog relacionado: BLG-0017 (CSP-002)
- Status: Aprovada para implementacao incremental

## 1. Contexto

Com o CSP-001 implementado, o MVP precisa aplicar a rubrica de listening (E2.S2) ao item curado para padronizar selecao e reduzir subjetividade.

## 2. Objetivo

Implementar o calculo de score ponderado da matriz de listening e gerar classificacao final do item avaliado.

## 3. Escopo

- representar criterios e pesos oficiais da matriz;
- validar notas por criterio no intervalo 0 a 5;
- calcular score final ponderado em escala 0 a 5;
- classificar resultado em faixas recomendadas pela documentacao.

## 4. Fora do escopo

- persistencia da avaliacao em banco;
- interface web para avaliacao;
- sincronizacao com Anki;
- deduplicacao e reconciliacao de itens.

## 5. Dependencias

- CSP-001 (entidade CuratedStudyItem);
- E2.S2 (matriz e pesos definidos).

## 6. Riscos

- aplicacao inconsistente de criterios por lote;
- notas fora de faixa sem validacao;
- divergencia entre score calculado e faixas de classificacao.

## 7. Metricas de sucesso

- 100% dos criterios obrigatorios validados;
- 100% dos testes de classificacao nas faixas oficiais aprovados;
- score final sempre em intervalo 0 a 5.

## 8. Criterios de conclusao

- modulo de avaliacao implementado com pesos oficiais;
- testes cobrindo calculo, validacao e faixas de classificacao;
- avaliacao aplicada a item curado com saida serializavel.

## 9. Entregaveis

- modulo de dominio de avaliacao de listening;
- testes unitarios da matriz;
- documentacao da SPEC registrada.

## 10. Plano incremental

1. Definir constantes de pesos e criterios.
2. Implementar validacoes de entrada e calculo ponderado.
3. Implementar classificacao final por faixa.
4. Cobrir com testes unitarios de aceite.

## 11. Rastreabilidade

- Roadmap: E5
- Backlog: BLG-0017 / CSP-002
- ADR relacionada: N/A neste incremento
- Changelog: secao Unreleased

## 12. Proximos passos

- Executar CSP-003 para mapear item e avaliacao para nota logica Anki.

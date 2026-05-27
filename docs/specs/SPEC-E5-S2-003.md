# SPEC-E5-S2-003 - Mapeamento para Nota Logica Anki

## Identificacao

- ID: SPEC-E5-S2-003
- Etapa: E5
- Subetapa: E5.S2
- Backlog relacionado: BLG-0017 (CSP-003)
- Status: Aprovada para implementacao incremental

## 1. Contexto

Com item curado (CSP-001) e avaliacao de listening (CSP-002) implementados, o proximo incremento do MVP e mapear esses dados para a estrutura logica de nota Anki definida em E4.S1.

## 2. Objetivo

Implementar o mapeamento deterministico de item + avaliacao para payload logico de nota, pronto para futura integracao AnkiConnect.

## 3. Escopo

- compor nome de deck por modulo/habilidade/nivel;
- mapear campos minimos da nota conforme E4.S1;
- normalizar e compor tags padronizadas;
- anexar metadados logicos de avaliacao e midia.

## 4. Fora do escopo

- chamada real ao AnkiConnect;
- criacao/atualizacao remota de nota;
- reconciliacao de duplicidade em servidor Anki;
- tratamento completo de excecoes de conectividade.

## 5. Dependencias

- CSP-001 (CuratedStudyItem);
- CSP-002 (ListeningEvaluation);
- E4.S1 (modelo logico).

## 6. Riscos

- inflacao ou inconsistencias de tags;
- payload com campos divergentes do contrato logico;
- deck mal composto para classificacao por nivel.

## 7. Metricas de sucesso

- 100% dos campos minimos de E4.S1 presentes no payload;
- 100% dos testes de deck e tags passando;
- identificador logico preservado para deduplicacao futura.

## 8. Criterios de conclusao

- mapeador implementado e testado;
- payload serializavel e deterministico;
- composicao de deck e tags validada.

## 9. Entregaveis

- modulo de mapeamento logico para Anki;
- testes unitarios de mapeamento;
- documentacao da SPEC registrada.

## 10. Plano incremental

1. Definir estrutura de saida da nota logica.
2. Implementar composicao de deck e fields.
3. Implementar normalizacao de tags e anexos logicos.
4. Validar com testes de contrato minimo.

## 11. Rastreabilidade

- Roadmap: E5
- Backlog: BLG-0017 / CSP-003
- ADR relacionada: N/A neste incremento
- Changelog: secao Unreleased

## 12. Proximos passos

- Preparar ambiente local de conexao com AnkiConnect (healthcheck e configuracao).
- Executar CSP-004 para deduplicacao logica e reconciliacao.

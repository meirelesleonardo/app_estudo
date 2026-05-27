# SPEC-E5-S2-001 - Entidade de Item de Estudo Curado

## Identificacao

- ID: SPEC-E5-S2-001
- Etapa: E5
- Subetapa: E5.S2
- Backlog relacionado: BLG-0017 (CSP-001)
- Status: Aprovada para implementacao incremental

## 1. Contexto

E5 definiu o MVP implementavel e priorizou candidatos a SPEC. O primeiro incremento (CSP-001) precisa estruturar a entidade de item curado para permitir consistencia de dados, validacao de preenchimento e rastreabilidade minima antes de qualquer automacao adicional.

## 2. Objetivo

Implementar uma entidade de dominio para representar um item de estudo curado de listening, com campos minimos obrigatorios e regras de validacao.

## 3. Escopo

- definir estrutura de dados do item curado;
- aplicar validacoes de obrigatoriedade e formato;
- padronizar serializacao para dicionario;
- expor chave logica estavel para reconciliacao futura.

## 4. Fora do escopo

- aplicacao de score da rubrica de listening (CSP-002);
- mapeamento completo para nota Anki (CSP-003);
- politica de deduplicacao e reconciliacao (CSP-004);
- trilha completa de historico/auditoria (CSP-005);
- execucao de lote piloto (CSP-006).

## 5. Dependencias

- E3 concluida (modelo de entidades e rastreabilidade);
- E4 concluida (modelo logico de nota e tags);
- E1 e E2 concluidas (classificacao pedagogica e matriz).

## 6. Riscos

- inconsistencias de preenchimento entre itens curados;
- taxonomia de tags sem padronizacao;
- identificacao logica fraca para reconciliacao futura.

## 7. Metricas de sucesso

- 100% dos itens de teste com campos obrigatorios validados;
- 100% dos cenarios invalidos criticos rejeitados;
- serializacao estavel para persistencia documental.

## 8. Criterios de conclusao

- entidade implementada com validacoes de campos minimos;
- testes unitarios cobrindo casos validos e invalidos essenciais;
- chave logica deterministica disponivel no modelo.

## 9. Entregaveis

- modulo de dominio para item curado;
- testes unitarios da entidade;
- documentacao da SPEC registrada.

## 10. Plano incremental

1. Implementar estrutura de dados e enums base.
2. Implementar validacoes de preenchimento e normalizacao de tags.
3. Adicionar serializacao e chave logica.
4. Validar com testes unitarios de aceite do incremento.

## 11. Rastreabilidade

- Roadmap: E5
- Backlog: BLG-0017 / CSP-001
- ADR relacionada: N/A neste incremento
- Changelog: secao Unreleased

## 12. Proximos passos

- Executar CSP-002 com base na entidade estabilizada.
- Evoluir para CSP-003 (mapeamento para nota logica Anki).

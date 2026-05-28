# SPEC-E2-S4-003 - Pipeline de Normalizacao Textual Versionada

## Identificacao

- ID: SPEC-E2-S4-003
- Etapa: E2
- Subetapa: E2.S4
- Backlog relacionado: BLG-0032 (CSP-E2-S4-003), BLG-0026, BLG-0029, BLG-0031
- Status: Concluida (implementacao inicial)

## 1. Contexto

Com contratos de origem e transcript definidos, o terceiro incremento precisa
formalizar um pipeline de normalizacao textual com governanca de versao,
sem descaracterizar oralidade relevante para listening.

## 2. Objetivo

Definir pipeline de normalizacao textual em etapas, com flags de transformacao,
versionamento de regra e criterios de qualidade para uso pedagogico.

## 3. Escopo

- definir etapas formais de normalizacao textual;
- definir tratamento para contractions, fillers, ruido e duplicidade;
- definir regras para sentencas incompletas e caracteres especiais;
- definir versionamento de regra de normalizacao;
- definir evidencia minima para auditoria de transformacao textual.

## 4. Fora do escopo

- implementacao de NLP/ML;
- correcao automatica contextual por IA generativa;
- segmentacao final em StudySegment;
- publicacao automatica no Anki.

## 5. Dependencias

- SPEC-E2-S4-002;
- E2.S3 (validacao de legenda/transcricao);
- E3.S3 (auditoria e historico);
- diretrizes de curadoria de E2.S1.

## 6. Riscos

- sobre-normalizacao remover sinais de fala natural importantes para aprendizado;
- sub-normalizacao manter ruido excessivo e reduzir clareza didatica;
- falta de versionamento inviabilizar reproducao e reprocessamento.

## 7. Metricas de sucesso

- etapas de pipeline documentadas com entrada/saida por fase;
- flags de transformacao definidas para 100% das classes de limpeza previstas;
- versao de regra obrigatoria em toda saida normalizada;
- criterios de aceitacao textual publicados para gate de qualidade.

## 8. Criterios de conclusao

- pipeline de normalizacao publicado com etapas e regras;
- tabela de flags e efeitos de transformacao publicada;
- politica de versionamento e reprocessamento conectada ao BLG-0029;
- checklist de auditoria textual publicado.

## 9. Entregaveis

- especificacao do pipeline de normalizacao textual;
- tabela de flags de transformacao e exemplos;
- politica de versionamento de normalizacao;
- checklist de auditoria de saida textual.

## 10. Plano incremental

1. Formalizar etapas do pipeline e regras por etapa.
2. Definir classes de transformacao e respectivas flags.
3. Definir versao de regra e criterio de reprocessamento.
4. Publicar checklist de qualidade para gate de validacao.

## 11. Rastreabilidade

- Roadmap: E2.S4
- Backlog: BLG-0032 / CSP-E2-S4-003, BLG-0026, BLG-0029, BLG-0031
- ADR relacionada: ADR-0001
- Changelog: secao Unreleased

## 12. Proximos passos

- Encadear com SPEC de segmentacao pedagogica (CSP-E2-S4-004).

## Evidencias de implementacao

- Modulo de dominio `transcript_normalization` implementado com pipeline versionado.
- Flags de transformacao para timestamps, contractions, fillers, ruido, duplicidade,
  espacos e sentenca incompleta implementadas.
- Regra de versao obrigatoria da normalizacao implementada.
- Testes unitarios adicionados para cenarios validos e invalidos da normalizacao.

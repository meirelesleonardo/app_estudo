# SPEC-E2-S4-004 - Estrategia de Segmentacao Pedagogica

## Identificacao

- ID: SPEC-E2-S4-004
- Etapa: E2
- Subetapa: E2.S4
- Backlog relacionado: BLG-0032 (CSP-E2-S4-004), BLG-0027, BLG-0031
- Status: Concluida (implementacao inicial)

## 1. Contexto

Com os contratos de origem/transcript e normalizacao definidos, o proximo incremento
precisa materializar uma estrategia de chunking pedagogico para evitar o anti-padrao
1 video = 1 card e preparar base para fluxo de estudo incremental.

## 2. Objetivo

Implementar segmentacao pedagogica em granularidade de segmento com limites operacionais,
preservando lineage para vinculo com transcript curado.

## 3. Escopo

- definir entidade StudySegment com contrato minimo de auditoria;
- segmentar texto curado em recortes pedagogicos;
- aplicar limites operacionais de duracao por segmento;
- gerar identificador deterministico por segmento;
- manter vinculo source_media_id e curated_transcript_id.

## 4. Fora do escopo

- segmentacao por alinhamento fonetico;
- extracao de audio por recorte;
- classificacao automatica por IA;
- sincronizacao com Anki.

## 5. Dependencias

- SPEC-E2-S4-003;
- E1.S2 (trilhas por dificuldade);
- E3.S2 e E3.S3 (vinculo e auditoria).

## 6. Riscos

- segmentos longos demais reduzirem foco pedagogico;
- segmentos curtos demais quebrarem contexto;
- distribuicao temporal inconsistente em textos heterogeneos.

## 7. Metricas de sucesso

- 100% dos segmentos com lineage e hash deterministico;
- segmentos com duracao dentro de limites operacionais por padrao;
- regra de particionamento reprodutivel para mesma entrada;
- cobertura de testes para cenarios validos e invalidos.

## 8. Criterios de conclusao

- entidade StudySegment implementada com validacoes;
- funcao de segmentacao implementada com limites min/max;
- testes unitarios de segmentacao adicionados;
- rastreabilidade atualizada para CSP-E2-S4-004.

## 9. Entregaveis

- modulo de dominio de segmentacao;
- entidade StudySegment;
- funcao de segmentacao de transcript curado;
- testes unitarios da estrategia.

## 10. Plano incremental

1. Definir contrato da entidade StudySegment.
2. Implementar particionamento por sentencas e agrupamento por janela.
3. Aplicar limites operacionais de duracao por segmento.
4. Gerar hash deterministico e validar por testes.

## 11. Rastreabilidade

- Roadmap: E2.S4
- Backlog: BLG-0032 / CSP-E2-S4-004, BLG-0027, BLG-0031
- ADR relacionada: ADR-0001
- Changelog: secao Unreleased

## 12. Proximos passos

- Evoluir para SPEC-E2-S4-005 (persistencia de metadados e hashes).

## Evidencias de implementacao

- Entidade `StudySegment` implementada com validacoes de contrato e faixa de duracao.
- Segmentador pedagogico implementado com particionamento por sentenca e janela temporal.
- Hash e IDs deterministas por segmento implementados.
- Testes unitarios cobrindo cenarios principais e de validacao adicionados.

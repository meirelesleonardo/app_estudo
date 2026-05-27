# Modelo de Rastreabilidade

## Objetivo

Garantir que toda decisao, requisito e item de backlog possam ser rastreados de ponta a ponta.

## Entidades

- Etapa (E#)
- Subetapa (E#.S#)
- Backlog (BLG-####)
- Decisao (ADR-####)
- SPEC (SPEC-...)
- Marco (M#)

## Regras

1. Todo item de backlog deve apontar para uma etapa.
2. Toda SPEC deve apontar para subetapa e backlog.
3. Toda ADR deve apontar para impactos em backlog e roadmap.
4. Mudancas de escopo devem atualizar roadmap e backlog no mesmo ciclo.

## Matriz de ligacao minima

- Etapa -> Subetapas
- Subetapa -> Backlog
- Backlog -> SPEC
- SPEC -> ADR (quando houver decisao relevante)
- Backlog -> Changelog (quando concluido)

## Regras complementares para ingestao de midia (E2.S4)

1. Todo artefato de origem deve manter identificador externo e hash de referencia.
2. Conteudo bruto (raw) e conteudo curado (curated) devem existir em entidades separadas.
3. Toda transformacao textual deve registrar versao de regra e timestamp de processamento.
4. Segmentos pedagogicos devem manter vinculo ao transcript curado e ao source de origem.
5. Nenhum artefato pode mudar para estado Operational sem evidencia minima de lineage.

## Regras complementares para Trusted Knowledge Sources (E2.S5)

1. Toda fonte deve possuir classificacao, confiabilidade, revisao, expiracao e mantenedor.
2. Fonte sem status approved ou review_required nao pode gerar automacao de IA.
3. Fonte experimental deve permanecer separada da base oficial de conhecimento.
4. Toda politica de uso por IA deve estar vinculada a criterio de risco observavel.
5. Mudanca de confiabilidade deve gerar evento de auditoria e nova versao.

## Evidencias minimas de lineage

- source_media_id e external_id preenchidos;
- referencia ao raw_transcript_id de origem;
- referencia ao curated_transcript_id (quando existir);
- hash do artefato atual;
- versao de normalizacao/curadoria;
- evento de auditoria com data e tipo de mudanca.

## Criterios de qualidade da rastreabilidade

- completude: links obrigatorios preenchidos;
- consistencia: IDs validos e sem duplicidade;
- atualidade: status alinhado entre roadmap e backlog;
- auditabilidade: historico de decisao registrado.

## Exemplo de fluxo

1. Definir E2.S1 (curadoria de fontes).
2. Criar BLG-0012 para matriz de avaliacao.
3. Refinar e aprovar SPEC-E2-S1-001.
4. Registrar ADR caso haja decisao de criterio.
5. Atualizar changelog no fechamento.

## Expansao em E3

- Modelo de entidades: [E3_ENTITY_MODEL.md](E3_ENTITY_MODEL.md)
- Regras de vinculo: [E3_ARTIFACT_LINKING_RULES.md](E3_ARTIFACT_LINKING_RULES.md)
- Auditoria e historico: [E3_AUDIT_AND_HISTORY.md](E3_AUDIT_AND_HISTORY.md)
- Matriz E2.S4: [E2_S4_TRACEABILITY_MATRIX.md](E2_S4_TRACEABILITY_MATRIX.md)
- Matriz E2.S5/E6: [E2_S5_E6_TRACEABILITY_MATRIX.md](E2_S5_E6_TRACEABILITY_MATRIX.md)

# SPEC-E2-S4-001 - Contrato de SourceMedia e SourceMetadata

## Identificacao

- ID: SPEC-E2-S4-001
- Etapa: E2
- Subetapa: E2.S4
- Backlog relacionado: BLG-0032 (CSP-E2-S4-001), BLG-0023, BLG-0024, BLG-0025
- Status: Proposta pronta para gate pre-SPEC

## 1. Contexto

A subetapa E2.S4 foi formalizada para ingestao e processamento de midia.
O primeiro incremento tecnico precisa fixar o contrato de origem para reduzir
ambiguidade nos dados de entrada e fortalecer rastreabilidade.

## 2. Objetivo

Definir contrato arquitetural de SourceMedia e SourceMetadata com atributos obrigatorios,
regras de identificacao univoca, classificacao de fonte e vinculos minimos de lineage.

## 3. Escopo

- definir campos obrigatorios e opcionais de SourceMedia;
- definir campos obrigatorios e opcionais de SourceMetadata;
- definir regra de unicidade por platform + external_id;
- definir validacoes minimas de qualidade de metadados;
- definir vinculos minimos para trilha de auditoria de origem.

## 4. Fora do escopo

- extracao automatica de legenda/audio;
- persistencia fisica em banco ou object storage;
- integracao tecnica com APIs externas;
- processamento de normalizacao textual.

## 5. Dependencias

- E2.S1 (curadoria de fontes);
- E2.S3 (validacao de legenda/transcricao);
- E3.S1 (modelo de entidades);
- ADR-0001 (YouTube como fonte oficial inicial de ingestao).

## 6. Riscos

- inconsistencias de identificacao da origem por ausencia de chave canonica;
- metadados incompletos comprometerem classificacao pedagogica;
- acoplamento precoce ao provedor de origem sem contrato neutro.

## 7. Metricas de sucesso

- 100% dos atributos obrigatorios documentados com tipo e regra de preenchimento;
- regra de unicidade definida e verificavel;
- criterios de qualidade de metadados vinculados a E2.S1;
- riscos e mitigacoes registrados no artefato.

## 8. Criterios de conclusao

- contrato SourceMedia publicado com atributos, vinculos e regras;
- contrato SourceMetadata publicado com atributos de curadoria;
- checklist de validacao de origem publicado;
- rastreabilidade atualizada para BLG e CSP relacionados.

## 9. Entregaveis

- especificacao documental de SourceMedia;
- especificacao documental de SourceMetadata;
- checklist de qualidade de metadados de origem;
- atualizacao de rastreabilidade em E2.S4.

## 10. Plano incremental

1. Consolidar atributos obrigatorios e opcionalidade de SourceMedia.
2. Consolidar atributos de classificacao em SourceMetadata.
3. Definir regra de identificacao univoca e conflito de origem.
4. Publicar checklist de validacao de origem para gate de entrada.

## 11. Rastreabilidade

- Roadmap: E2.S4
- Backlog: BLG-0032 / CSP-E2-S4-001, BLG-0023, BLG-0024, BLG-0025
- ADR relacionada: ADR-0001
- Changelog: secao Unreleased

## 12. Proximos passos

- Evoluir para SPEC-E2-S4-002 com separacao raw/curated e lineage textual.

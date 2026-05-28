# SPEC-E2-S4-005 - Persistencia de Metadados e Hashes em SQLite

## Identificacao

- ID: SPEC-E2-S4-005
- Etapa: E2
- Subetapa: E2.S4
- Backlog relacionado: BLG-0032 (CSP-E2-S4-005), BLG-0028, BLG-0031
- Status: Concluida (implementacao inicial)

## 1. Contexto

Com contratos de origem/transcript e segmentacao implementados, o proximo incremento
necessario e persistir artefatos e hashes em armazenamento estruturado com trilha
de auditoria para reprocessamento e compliance de lineage.

## 2. Objetivo

Implementar persistencia SQLite para SourceMedia, SourceMetadata, RawTranscript,
CuratedTranscript e StudySegment, com eventos auditaveis por artefato.

## 3. Escopo

- criar schema SQLite com tabelas de artefatos de E2.S4;
- suportar operacoes de upsert para todos os artefatos do pipeline atual;
- registrar eventos de auditoria por artefato persistido;
- expor consultas basicas de contagem e auditoria.

## 4. Fora do escopo

- migracao entre bancos em producao;
- replicacao distribuida;
- tuning avancado de performance;
- extracao direta de YouTube.

## 5. Dependencias

- SPEC-E2-S4-001
- SPEC-E2-S4-002
- SPEC-E2-S4-003
- SPEC-E2-S4-004
- E3.S3 (auditoria e historico)

## 6. Riscos

- inconsistencias de linkage se FKs nao forem aplicadas;
- perda de trilha se eventos de auditoria nao forem persistidos junto ao upsert;
- drift de hashes se serializacao nao for deterministica.

## 7. Metricas de sucesso

- 100% dos artefatos de E2.S4 com persistencia via SQLite;
- eventos de auditoria emitidos para cada upsert de artefato;
- schema com integridade referencial ativa;
- cobertura de testes para persistencia e upsert sem duplicacao.

## 8. Criterios de conclusao

- store SQLite implementado com schema e metodos de upsert;
- testes unitarios para persistencia e auditoria aprovados;
- export do store no pacote de integracoes;
- rastreabilidade atualizada para CSP-E2-S4-005.

## 9. Entregaveis

- modulo de integracao SQLite para artefatos de midia;
- schema com tabelas de artefatos e tabela de auditoria;
- testes unitarios de integridade e auditoria;
- registro de evidencias no changelog e diario.

## 10. Plano incremental

1. Definir schema SQLite e FKs para lineage.
2. Implementar upsert por tipo de artefato.
3. Implementar trilha de auditoria por artefato persistido.
4. Cobrir cenarios de persistencia e update por testes.

## 11. Rastreabilidade

- Roadmap: E2.S4
- Backlog: BLG-0032 / CSP-E2-S4-005, BLG-0028, BLG-0031
- ADR relacionada: ADR-0001
- Changelog: secao Unreleased

## 12. Proximos passos

- Evoluir para SPEC-E2-S4-006 (politica de versionamento e reprocessamento).

## Evidencias de implementacao

- Store `SqliteMediaArtifactStore` implementado com schema SQLite para artefatos E2.S4.
- Upsert de SourceMedia, SourceMetadata, RawTranscript, CuratedTranscript e StudySegment implementado.
- Tabela de `audit_event` com hash e metadados por operacao implementada.
- Testes unitarios de persistencia e auditoria aprovados.

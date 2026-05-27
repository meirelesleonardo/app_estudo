# E2.S4 - Plano Semanal de Execucao (Backlog -> Evidencia)

## Objetivo

Executar BLG-0023 a BLG-0029 em ciclos curtos, com gate por semana e evidencia objetiva,
sem iniciar implementacao tecnica.

## Premissas

- manter nomenclaturas e IDs ja publicados;
- evitar acoplamento alto entre frentes;
- publicar evidencia no mesmo ciclo de atualizacao do backlog;
- usar lifecycle oficial: Draft, Refining, Approved, Implementing, Validating, Operational, Deprecated.

## Planejamento semanal sugerido

| Semana | Foco | Backlog alvo | Dependencias principais | Criterio de conclusao observavel | Gate da semana | Evidencia obrigatoria |
|---|---|---|---|---|---|---|
| Semana 1 | Fundacao arquitetural E2.S4 | BLG-0023 | BLG-0007, BLG-0008, BLG-0009 | Documento arquitetural de E2.S4 publicado com escopo, pipeline e limites | Gate de definicao aprovado | Documento E2.S4 + atualizacao de roadmap/backlog |
| Semana 2 | Contrato de entidades de midia | BLG-0024 | BLG-0023, BLG-0012 | Entidades SourceMedia, RawTranscript, CuratedTranscript, StudySegment, NormalizedSentence, SourceMetadata formalizadas | Gate de rastreabilidade aprovado | Secao de entidades com atributos, vinculos e riscos |
| Semana 3 | Estrategia de origem YouTube + normalizacao | BLG-0025, BLG-0026 | BLG-0024, BLG-0009 | Contrato de origem YouTube e pipeline de normalizacao com regras e versoes publicados | Gate de risco aprovado | Criterios de origem + etapas de normalizacao + riscos/mitigacoes |
| Semana 4 | Segmentacao e persistencia | BLG-0027, BLG-0028 | BLG-0026, BLG-0013, BLG-0014 | Estrategia de chunking e persistencia/hashes definida com separacao raw-curated | Gate de evidencia aprovado | Regras de segmentacao + campos minimos de persistencia + lineage |
| Semana 5 | Versionamento e reprocessamento | BLG-0029 | BLG-0028, BLG-0014 | Politicas de atualizacao, substituicao, reconciliacao, invalidacao e reprocessamento publicadas | Gate de coerencia aprovado | Politica formal versionada + impactos documentados |
| Semana 6 | Consolidacao para candidatos a SPEC | BLG-0032 | BLG-0023 a BLG-0029 | Backlog tecnico E2.S4 fechado com candidatos a SPEC, dependencias e criterios observaveis | Gate pre-SPEC aprovado | Documento de backlog tecnico E2.S4 + vinculos de rastreabilidade |

## Definicao de gate por semana

1. Gate de definicao
- escopo, nao escopo e objetivo declarados.

2. Gate de rastreabilidade
- vinculos com etapa/subetapa/backlog e impactos declarados.

3. Gate de risco
- riscos principais e mitigacoes registrados.

4. Gate de evidencia
- artefato publicado e criterio de conclusao verificavel.

5. Gate de coerencia
- ausencia de conflito com historico operacional e SPECs aprovadas.

6. Gate pre-SPEC
- checklist de pronto para refinamento tecnico aprovado.

## Controle operacional por item

Para cada backlog BLG-0023 a BLG-0029, registrar:

- estado de lifecycle atual;
- data de transicao de estado;
- evidencias vinculadas;
- riscos abertos;
- pendencias para o proximo gate.

## Rastreabilidade

- Etapa/Subetapa: E2.S4
- Backlog: BLG-0023, BLG-0024, BLG-0025, BLG-0026, BLG-0027, BLG-0028, BLG-0029, BLG-0032
- Dependencias: BLG-0007, BLG-0008, BLG-0009, BLG-0012, BLG-0013, BLG-0014

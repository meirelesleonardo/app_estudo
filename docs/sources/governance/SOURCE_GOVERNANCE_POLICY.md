# E2.S5 - Source Governance Policy

## Objetivo

Formalizar Knowledge Governance para Trusted Knowledge Sources,
com criterios de confiabilidade, validade e uso pela IA.

## Escopo

- classificacao de fontes;
- confiabilidade e risco;
- politicas de revisao, expiracao e versionamento;
- politicas de auditoria;
- politicas de uso por IA.

## Classificacao oficial de fontes

- oficial;
- normativa;
- operacional;
- pedagogica;
- comunitaria;
- experimental;
- laboratorio;
- audiovisual;
- documental.

## Niveis de confiabilidade

- alta;
- media;
- baixa;
- experimental.

## Atributos obrigatorios por fonte

Cada fonte deve possuir:
- source_id unico;
- categoria;
- subcategoria;
- nivel de confiabilidade;
- origem oficial;
- data de revisao;
- data de expiracao;
- idioma;
- formato;
- estrategia de uso;
- risco;
- observacoes;
- status;
- versao;
- mantenedor.

## Politica de revisao

- revisao mensal para fontes em uso operacional;
- revisao quinzenal para fonte audiovisual de alto volume;
- revisao imediata quando houver mudanca normativa critica.

## Politica de expiracao

- fonte expirada muda para status blocked_for_ai;
- fonte sem mantenedor muda para status blocked_for_ai;
- fonte sem revisao no prazo muda para status review_required.

## Politica de versionamento

- versao major para mudanca estrutural de contrato da fonte;
- versao minor para ajuste de metadado ou classificacao;
- versao patch para correcao editorial sem impacto de uso.

## Politica de auditoria

Eventos minimos:
- source_created;
- source_reviewed;
- source_reclassified;
- source_expired;
- source_reapproved;
- source_deprecated.

Cada evento deve registrar:
- source_id;
- versao;
- status anterior e status novo;
- responsavel;
- timestamp;
- justificativa.

## Politica de uso pela IA

Regras de autorizacao:
- AUTO_CARD_ALLOWED: oficial, normativa ou pedagogica com confiabilidade alta e status approved;
- HUMAN_REVIEW_REQUIRED: operacional ou comunitaria, ou confiabilidade media;
- SIMULATED_EXAM_ALLOWED: fonte de concurso curada por banca, com rastreabilidade de recorrencia;
- LAB_ALLOWED: laboratorio/operacional com checklist de seguranca aprovado;
- AUTOMATION_PROHIBITED: experimental, baixa confiabilidade, expirada ou sem mantenedor.

## Rastreabilidade

- Etapa/Subetapa: E2.S5
- Backlog: BLG-0033, BLG-0035, BLG-0036

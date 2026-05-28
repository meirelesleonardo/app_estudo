# E7 - Backlog Tecnico Incremental (Produto e Servico)

## Objetivo

Planejar a evolucao do projeto para operacao como servico,
com foco em fluxo self-service, demo publica e integracao assistida com Anki,
sem comprometer a governanca e rastreabilidade ja consolidadas em E0-E6.

## Escopo funcional da etapa

- Cliente seleciona objetivo de estudo/exercicio por trilha.
- Cliente seleciona videos/fontes a serem explorados.
- Sistema gera conteudo curado e estrutura de treino.
- Sistema sincroniza cards no Anki com controle de duplicidade e historico.
- Demo publica apresenta fluxo reduzido para validacao de interesse na landing page.

## Candidatos a SPEC

| Candidato | Objetivo | Dependencias | Criterio de conclusao |
|---|---|---|---|
| CSP-E7-001 | Definir fluxo self-service ponta a ponta | E2.S4, E4.S2, E5.S1 | Jornada de usuario com estados, entradas, saidas e falhas publicada |
| CSP-E7-002 | Definir contrato de onboarding de fontes/videos | E2.S5, ADR-0001 | Contrato com validacoes minimas, limites operacionais e politica de uso publicado |
| CSP-E7-003 | Definir estrategia de sync Anki por conta/perfil | E4.S1, E4.S2, CSP-004, CSP-005 | Politica de deduplicacao, reconciliacao e auditoria por cliente formalizada |
| CSP-E7-004 | Definir Demo Mode para landing page | CSP-E7-001 | Fluxo de demo guiada com dados controlados, metricas de uso e CTA validado |
| CSP-E7-005 | Definir modelo comercial inicial e limites de plano | CSP-E7-004 | Regras de plano (free/demo/pro), quotas e eventos de billing publicadas |
| CSP-E7-006 | Definir baseline de observabilidade e suporte | CSP-E7-001, CSP-E7-003 | Eventos minimos, logs de produto e runbook de suporte publicados |

## Priorizacao sugerida

1. CSP-E7-001
2. CSP-E7-004
3. CSP-E7-003
4. CSP-E7-002
5. CSP-E7-006
6. CSP-E7-005

## Politica de passagem para SPEC

Um candidato so vira SPEC quando:
- passar no gate pre-SPEC;
- tiver backlog vinculado;
- tiver risco, dependencia e impacto legal explicitados;
- tiver criterio de conclusao observavel;
- tiver evidencia de aderencia a governanca de fontes (E2.S5).

## Riscos e notas

- Termos de uso e direitos autorais de fontes audiovisuais devem ser tratados como risco de primeira ordem.
- Demo publica deve operar com conteudo controlado e politicas explicitas de uso.
- Integracao Anki deve priorizar confiabilidade e reversibilidade de operacoes.

## Rastreabilidade

- Etapa/Subetapa: E7
- Backlog: BLG-0045, BLG-0046, BLG-0047, BLG-0048, BLG-0049, BLG-0050

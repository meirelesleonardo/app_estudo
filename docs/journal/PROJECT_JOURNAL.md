# Diario do Projeto

## Objetivo

Registrar evolucao, decisoes e aprendizados por sessao.

## Entrada sugerida

- Data:
- Etapa/Subetapa:
- Itens de backlog trabalhados:
- Decisoes tomadas:
- Riscos identificados:
- Proximo passo:

## Primeira entrada

- Data: 2026-05-26
- Etapa/Subetapa: E0
- Itens de backlog trabalhados: BLG-0001, BLG-0002, BLG-0003
- Decisoes tomadas: iniciar por arquitetura documental e governanca
- Riscos identificados: tentar implementar sem refinamento
- Proximo passo: iniciar refinamento de E1 e E2

## Segunda entrada

- Data: 2026-05-26
- Etapa/Subetapa: E1
- Itens de backlog trabalhados: BLG-0004, BLG-0005, BLG-0006
- Decisoes tomadas: adotar trilhas A1-C1 com criterios objetivos por ciclo
- Riscos identificados: progressao sem limiar minimo por nivel
- Proximo passo: concluir E2 com validacao de legendas/transcricoes

## Terceira entrada

- Data: 2026-05-26
- Etapa/Subetapa: E2.S3
- Itens de backlog trabalhados: BLG-0009
- Decisoes tomadas: instituir rubrica e limiar de aprovacao para legenda/transcricao
- Riscos identificados: divergencia entre audio e texto em fontes sem revisao periodica
- Proximo passo: iniciar E3 (modelo de entidades de rastreabilidade)

## Quarta entrada

- Data: 2026-05-26
- Etapa/Subetapa: E3
- Itens de backlog trabalhados: BLG-0012, BLG-0013, BLG-0014
- Decisoes tomadas: formalizar entidades, matriz de vinculo e politica de auditoria como base obrigatoria para SPECs futuras
- Riscos identificados: crescimento documental sem consistencia de vinculos entre artefatos
- Proximo passo: iniciar E4 com arquitetura logica de Anki

## Quinta entrada

- Data: 2026-05-26
- Etapa/Subetapa: E4
- Itens de backlog trabalhados: BLG-0010, BLG-0015, BLG-0016
- Decisoes tomadas: separar integracao Anki em modelo logico, fluxos de sincronizacao e tratamento explicito de excecoes
- Riscos identificados: duplicidade, conflito de tags e perda de rastreabilidade em falhas de sincronizacao
- Proximo passo: iniciar E5 com definicao do MVP implementavel

## Sexta entrada

- Data: 2026-05-26
- Etapa/Subetapa: E5
- Itens de backlog trabalhados: BLG-0011, BLG-0017, BLG-0018
- Decisoes tomadas: definir recorte minimo do MVP, quebrar em candidatos a SPEC e formalizar criterio de pronto para implementacao
- Riscos identificados: iniciar desenvolvimento sem gate aprovado e sem recorte incremental
- Proximo passo: planejar transicao de foco para E6

## Setima entrada

- Data: 2026-05-26
- Etapa/Subetapa: E6
- Itens de backlog trabalhados: BLG-0019, BLG-0020, BLG-0021
- Decisoes tomadas: iniciar E6 com macroplano e detalhar S1-S3 mantendo incremento controlado
- Riscos identificados: expansao ampla sem priorizacao por edital e sem limiares objetivos de adaptatividade
- Proximo passo: fechar pendencias de S1-S3 e preparar criterios de conclusao de E6

## Oitava entrada

- Data: 2026-05-26
- Etapa/Subetapa: E5.S2
- Itens de backlog trabalhados: BLG-0017 (CSP-001)
- Decisoes tomadas: aprovar SPEC-E5-S2-001 e iniciar implementacao da entidade de item curado com validacoes minimas
- Riscos identificados: validar taxonomia inicial de tags antes de escalar volume de itens
- Proximo passo: implementar CSP-002 com aplicacao da matriz de avaliacao de listening

## Nona entrada

- Data: 2026-05-26
- Etapa/Subetapa: E5.S2
- Itens de backlog trabalhados: BLG-0017 (CSP-002)
- Decisoes tomadas: aprovar SPEC-E5-S2-002 e implementar calculo ponderado com faixas oficiais de classificacao
- Riscos identificados: variacao de avaliacao manual por criterio sem calibracao entre ciclos
- Proximo passo: implementar CSP-003 para mapear item e avaliacao para nota logica Anki

## Decima entrada

- Data: 2026-05-26
- Etapa/Subetapa: E5.S2
- Itens de backlog trabalhados: BLG-0017 (CSP-003)
- Decisoes tomadas: aprovar SPEC-E5-S2-003 e implementar mapeamento logico de item+avaliacao para nota Anki com deck, fields, tags e midia
- Riscos identificados: variacao de taxonomia de tags pode causar divergencia entre lotes se nao houver controle de versao
- Proximo passo: preparar cliente de conectividade e healthcheck para iniciar chamadas AnkiConnect

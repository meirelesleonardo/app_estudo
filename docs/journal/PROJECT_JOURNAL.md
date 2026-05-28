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

## Decima nona entrada

- Data: 2026-05-27
- Etapa/Subetapa: E6
- Itens de backlog trabalhados: BLG-0020, BLG-0021, BLG-0022
- Decisoes tomadas: consolidar edital referencia, taxonomia inicial, matriz de simulados, limiares adaptativos e catalogo inicial de laboratorios
- Riscos identificados: necessidade de calibracao continua dos limiares com dados reais de execucao
- Proximo passo: revisar governanca para ciclo operacional continuo

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

## Decima primeira entrada

- Data: 2026-05-26
- Etapa/Subetapa: E4.S2
- Itens de backlog trabalhados: BLG-0015
- Decisoes tomadas: implementar cliente base de AnkiConnect com sync create/update e mapeamento de estados pending, synced, updated, conflict e blocked
- Riscos identificados: sem politica formal de deduplicacao completa, conflitos multiplos permanecem dependentes do proximo incremento
- Proximo passo: evoluir para politica de deduplicacao e reconciliacao (CSP-004)

## Decima segunda entrada

- Data: 2026-05-26
- Etapa/Subetapa: E4.S2
- Itens de backlog trabalhados: BLG-0015
- Decisoes tomadas: ajustar cliente para criar modelo e deck automaticamente antes do sync e executar smoke test real com create/update bem sucedido
- Riscos identificados: manter padrao de nomes de deck e modelo para evitar proliferacao de estruturas no Anki
- Proximo passo: implementar CSP-004 para deduplicacao e reconciliacao de conflitos

## Decima terceira entrada

- Data: 2026-05-27
- Etapa/Subetapa: E4.S2
- Itens de backlog trabalhados: BLG-0015
- Decisoes tomadas: migrar deck legacy English para padrao Ingles::Listening::B1 reaproveitando notas adaptaveis e removendo estrutura antiga vazia
- Riscos identificados: revisar qualidade pedagogica das notas migradas legacy antes de consolidar ciclos de revisao
- Proximo passo: executar saneamento qualitativo das notas legacy e iniciar CSP-004

## Decima quarta entrada

- Data: 2026-05-27
- Etapa/Subetapa: E4.S2
- Itens de backlog trabalhados: BLG-0015
- Decisoes tomadas: executar saneamento qualitativo automatico em 45 notas de Ingles::Listening::B1 removendo tags legacy e normalizando metadados para pending_review
- Riscos identificados: ainda ha necessidade de curadoria manual pontual de explicacoes para maximizar retencao
- Proximo passo: iniciar CSP-004 com politica de deduplicacao e reconciliacao

## Decima quinta entrada

- Data: 2026-05-27
- Etapa/Subetapa: E5.S2
- Itens de backlog trabalhados: BLG-0017 (CSP-004)
- Decisoes tomadas: implementar reconciliacao de duplicatas por source_id com estrategias keep_oldest/keep_newest e execucao dry-run/apply
- Riscos identificados: reconciliacao automatica ainda depende de revisao humana em casos sem source_id confiavel
- Proximo passo: evoluir CSP-005 com trilha de historico de alteracoes por item

## Decima sexta entrada

- Data: 2026-05-27
- Etapa/Subetapa: E5.S2
- Itens de backlog trabalhados: BLG-0017 (CSP-005)
- Decisoes tomadas: implementar store JSONL de historico por item, integrar registro automatico no cliente Anki e validar consulta por script
- Riscos identificados: definir politica de retencao/rotacao do historico local para crescimento de longo prazo
- Proximo passo: iniciar CSP-006 com lote piloto e criterios de aceite do MVP

## Decima setima entrada

- Data: 2026-05-27
- Etapa/Subetapa: E5.S2
- Itens de backlog trabalhados: BLG-0017 (CSP-006)
- Decisoes tomadas: iniciar validacao automatizada do lote piloto com thresholds explicitos de rastreabilidade, duplicidade e classificacao pedagogica
- Riscos identificados: lote pequeno pode distorcer metricas e gerar aprovacao estatisticamente fraca
- Proximo passo: executar validacao no deck real e tratar lacunas ate status approved consistente

## Decima oitava entrada

- Data: 2026-05-27
- Etapa/Subetapa: E5.S2
- Itens de backlog trabalhados: BLG-0017 (CSP-006)
- Decisoes tomadas: aplicar backfill controlado de evaluation_score e audio_reference, mantendo tag explicita para referencias de audio pendentes
- Riscos identificados: valores preenchidos como placeholders exigem curadoria posterior para substituicao por links reais de audio
- Proximo passo: consolidar gate final do MVP com plano de substituicao gradual dos placeholders de audio

## Decima nona entrada

- Data: 2026-05-27
- Etapa/Subetapa: E5.S3
- Itens de backlog trabalhados: BLG-0018
- Decisoes tomadas: consolidar checklist final de pronto para implementacao com evidencias operacionais dos incrementos CSP-001 a CSP-006
- Riscos identificados: manter rastreabilidade aprovada sem degradar qualidade semantica dos campos preenchidos por backfill
- Proximo passo: abrir ciclo de operacao controlada do MVP e plano de curadoria continua para audio_reference real

## Vigesima entrada

- Data: 2026-05-27
- Etapa/Subetapa: E2.S4
- Itens de backlog trabalhados: BLG-0032, BLG-0023, BLG-0024, BLG-0025, BLG-0026
- Decisoes tomadas: aprovar gate pre-SPEC unificado para SPEC-E2-S4-001, SPEC-E2-S4-002 e SPEC-E2-S4-003 com status GO sequencial
- Riscos identificados: iniciar implementacao fora da ordem de dependencias pode comprometer lineage e auditoria de transcript
- Proximo passo: iniciar implementacao da SPEC-E2-S4-001 e registrar evidencia incremental por SPEC

## Vigesima primeira entrada

- Data: 2026-05-27
- Etapa/Subetapa: E2.S4
- Itens de backlog trabalhados: BLG-0032 (CSP-E2-S4-001), BLG-0024, BLG-0025
- Decisoes tomadas: implementar entidades SourceMedia e SourceMetadata com contrato minimo de origem/metadados e chave logica platform+external_id
- Riscos identificados: manter neutralidade de contrato para futuras plataformas sem perder rigor nas validacoes atuais
- Proximo passo: iniciar SPEC-E2-S4-002 com separacao formal de RawTranscript e CuratedTranscript

# Changelog

Todas as mudancas relevantes deste projeto serao registradas aqui.

Formato inspirado em Keep a Changelog e versionamento semantico quando houver releases de implementacao.

## [Unreleased]

### Added
- Estrutura documental inicial.
- Governanca base do projeto.
- Roadmap incremental com etapas E0-E6.
- Refinamento detalhado de E1 (objetivos e trilhas A1-C1).
- Catalogo inicial de fontes de E2.
- Estrategia formal de validacao de legendas/transcricoes (E2.S3).
- Modelo de entidades de rastreabilidade (E3.S1).
- Regras de vinculo entre artefatos (E3.S2).
- Politica de auditoria e historico de mudancas (E3.S3).
- Modelo logico de integracao com Anki (E4.S1).
- Fluxos logicos de sincronizacao com Anki (E4.S2).
- Tratamento de excecoes e divergencias da integracao (E4.S3).
- Escopo minimo do MVP implementavel (E5.S1).
- Backlog tecnico incremental com candidatos a SPEC (E5.S2).
- Criterio formal de pronto para implementacao (E5.S3).
- Plano de expansao para concursos e Defesa Cibernetica (E6).
- Estrutura inicial de curadoria tecnica por edital e disciplina (E6.S1).
- Blueprint inicial de questoes e simulados (E6.S2).
- Modelo inicial de trilhas adaptativas e laboratorios (E6.S3).
- Relatorio unico de prontidao e consistencia das etapas E0-E6.
- Primeira SPEC de implementacao: SPEC-E5-S2-001 (CSP-001).
- Estrutura inicial de codigo Python com pacote app_estudo.
- Entidade de dominio CuratedStudyItem com validacoes de campos minimos e chave logica deterministica.
- Testes unitarios iniciais para validacao da entidade de item curado.
- Segunda SPEC de implementacao: SPEC-E5-S2-002 (CSP-002).
- Matriz de avaliacao de listening com pesos oficiais, score final e classificacao por faixa.
- Testes unitarios para validacao de criterios obrigatorios, faixa de notas e classificacao final.
- Terceira SPEC de implementacao: SPEC-E5-S2-003 (CSP-003).
- Mapeador logico para nota Anki com deck, campos minimos, tags compostas e metadados de midia.
- Guia de preparacao do ambiente local para AnkiConnect.
- Testes unitarios para contrato de mapeamento item+avaliacao para payload logico Anki.
- Modulo de healthcheck de AnkiConnect para validar endpoint local e versao.
- Script CLI para verificar prontidao de conexao com AnkiConnect.
- SPEC-E4-S2-001 para cliente base de sincronizacao com AnkiConnect.
- Cliente AnkiConnect com fluxo basico de sync (create/update) e estados logicos de retorno.
- Testes unitarios do cliente para cenarios de synced, updated, conflict, pending e blocked.
- Ajuste de compatibilidade do cliente para criar automaticamente modelo e deck antes da sincronizacao.
- Smoke test real com Anki aberto validando fluxo create/update com sucesso.
- Script de padronizacao de deck legacy para migrar cards ao padrao Ingles::Listening::<nivel>.
- Migracao aplicada no deck English com consolidacao dos cards em Ingles::Listening::B1 e remocao do deck vazio.
- Script de saneamento qualitativo para normalizar tags e metadados das notas migradas.
- Saneamento aplicado em 45 notas com remocao de marcadores legacy e padrao pending_review.
- Quarta SPEC de implementacao: SPEC-E5-S2-004 (CSP-004).
- Modulo de reconciliacao de duplicatas por source_id com estrategias keep_oldest/keep_newest.
- Script CLI de reconciliacao com modo dry-run e modo apply.
- Quinta SPEC de implementacao: SPEC-E5-S2-005 (CSP-005).
- Modulo de historico por item em arquivo JSONL para eventos de sync e reconciliacao.
- Script de consulta do historico com filtros por item, tipo de evento e limite.
- Sexta SPEC de implementacao: SPEC-E5-S2-006 (CSP-006).
- Modulo de validacao de lote piloto com metricas de aceite do MVP.
- Script operacional para validar lote piloto diretamente no deck alvo.
- Backfill operacional de campos faltantes do lote piloto (evaluation_score e audio_reference) com script dedicado.
- Validacao real do lote Ingles::Listening::B1 com status final approved e criterios de aceite atendidos.
- Fechamento do gate final do MVP com checklist de aceite marcado e consolidacao de evidencias CSP-001 a CSP-006.
- Guia de instalacao e preparacao do Anki/AnkiConnect ampliado com passo a passo para Linux Mint e Windows 11.
- Guia de usabilidade do app com jornada operacional, checklist e boas praticas de execucao.
- Guia rapido de onboarding (Quick Start) para validacao minima do ambiente e execucao inicial.
- Padronizacao dos docs de integracao no template comum: Objetivo, Pre-requisitos, Passos, Validacao, Troubleshooting e Rastreabilidade.
- Template reutilizavel para novas docs de integracao em docs/integrations/INTEGRATION_DOC_TEMPLATE.md.

### Changed
- Status de E2 atualizado para concluida no roadmap.
- BLG-0009 marcado como concluido no backlog inicial.
- Status de E3 atualizado para concluida no roadmap.
- Status de E4 atualizado para concluida no roadmap.
- Status de E5 atualizado para concluida no roadmap.
- Status de E6 atualizado para concluida no roadmap.

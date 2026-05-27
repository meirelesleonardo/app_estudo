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

### Changed
- Status de E2 atualizado para concluida no roadmap.
- BLG-0009 marcado como concluido no backlog inicial.
- Status de E3 atualizado para concluida no roadmap.
- Status de E4 atualizado para concluida no roadmap.
- Status de E5 atualizado para concluida no roadmap.
- Status de E6 atualizado para em andamento no roadmap.

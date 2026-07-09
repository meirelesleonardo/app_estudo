# Automacao Inteligente de Estudos com IA + Anki

Projeto open source para planejamento e futura implementacao incremental de uma plataforma de automacao de estudos com IA, integracao com Anki e trilhas de revisao espacada.

## Estado Atual

Fase: Transicao para implementacao incremental (primeira SPEC em execucao)

Neste momento, o repositorio esta focado em:
- arquitetura macro;
- governanca do projeto;
- roadmap incremental;
- backlog inicial;
- estrategia de rastreabilidade;
- planejamento de integracoes futuras;
- implementacao inicial do dominio (CSP-001 / SPEC-E5-S2-001).

## Objetivos

- Criar um sistema reutilizavel de estudos orientado por dados.
- Comecar pelo modulo de ingles (listening e connected speech).
- Evoluir para concursos publicos com foco em Defesa Cibernetica.
- Servir como laboratorio pessoal de IA aplicada e portfolio tecnico.

## Principios de Execucao

- Documentacao antes de implementacao.
- Evolucao em etapas pequenas, rastreaveis e validadas.
- Nada de codigo sem escopo e criterios de conclusao definidos.
- Cada etapa precisa declarar: contexto, objetivo, escopo, nao escopo, riscos, metricas e entregaveis.

## Roadmap de Alto Nivel

1. Fundacao documental e governanca.
2. Modulo de ingles: curadoria de fontes e estrategia de listening.
3. Arquitetura de dados e modelo de rastreabilidade.
4. Planejamento da integracao com AnkiConnect.
5. MVP documental pronto para inicio de implementacao guiada.
6. Expansao para concursos e Defesa Cibernetica.

Detalhes completos em [ROADMAP.md](ROADMAP.md).

## Estrutura de Documentacao

- [docs/architecture/MACRO_ARCHITECTURE.md](docs/architecture/MACRO_ARCHITECTURE.md)
- [docs/governance/PROJECT_GOVERNANCE.md](docs/governance/PROJECT_GOVERNANCE.md)
- [docs/governance/PRE_SPEC_GATE.md](docs/governance/PRE_SPEC_GATE.md)
- [docs/traceability/TRACEABILITY_MODEL.md](docs/traceability/TRACEABILITY_MODEL.md)
- [docs/traceability/E3_ENTITY_MODEL.md](docs/traceability/E3_ENTITY_MODEL.md)
- [docs/traceability/E3_ARTIFACT_LINKING_RULES.md](docs/traceability/E3_ARTIFACT_LINKING_RULES.md)
- [docs/traceability/E3_AUDIT_AND_HISTORY.md](docs/traceability/E3_AUDIT_AND_HISTORY.md)
- [docs/english/ENGLISH_MODULE_PLAN.md](docs/english/ENGLISH_MODULE_PLAN.md)
- [docs/english/E1_REFINEMENT.md](docs/english/E1_REFINEMENT.md)
- [docs/english/E1_LEVEL_TRACKS_A1_C1.md](docs/english/E1_LEVEL_TRACKS_A1_C1.md)
- [docs/english/E2_INITIAL_SOURCE_CATALOG.md](docs/english/E2_INITIAL_SOURCE_CATALOG.md)
- [docs/english/E2_SUBTITLE_TRANSCRIPT_VALIDATION.md](docs/english/E2_SUBTITLE_TRANSCRIPT_VALIDATION.md)
- [docs/english/SOURCE_CURATION_STRATEGY.md](docs/english/SOURCE_CURATION_STRATEGY.md)
- [docs/integrations/ANKI_INTEGRATION_STRATEGY.md](docs/integrations/ANKI_INTEGRATION_STRATEGY.md)
- [docs/integrations/ANKI_ENV_SETUP.md](docs/integrations/ANKI_ENV_SETUP.md)
- [docs/integrations/INTEGRATION_DOC_TEMPLATE.md](docs/integrations/INTEGRATION_DOC_TEMPLATE.md)
- [docs/usability/APP_USABILITY_GUIDE.md](docs/usability/APP_USABILITY_GUIDE.md)
- [docs/usability/QUICK_START.md](docs/usability/QUICK_START.md)
- [docs/integrations/E4_LOGICAL_MODEL.md](docs/integrations/E4_LOGICAL_MODEL.md)
- [docs/integrations/E4_SYNC_FLOWS.md](docs/integrations/E4_SYNC_FLOWS.md)
- [docs/integrations/E4_EXCEPTION_HANDLING.md](docs/integrations/E4_EXCEPTION_HANDLING.md)
- [docs/specs/SPEC_WORKFLOW.md](docs/specs/SPEC_WORKFLOW.md)
- [docs/specs/E5_MVP_SCOPE.md](docs/specs/E5_MVP_SCOPE.md)
- [docs/backlog/E5_TECHNICAL_BACKLOG.md](docs/backlog/E5_TECHNICAL_BACKLOG.md)
- [docs/governance/E5_READY_FOR_IMPLEMENTATION.md](docs/governance/E5_READY_FOR_IMPLEMENTATION.md)
- [docs/cybersec/E6_EXPANSION_PLAN.md](docs/cybersec/E6_EXPANSION_PLAN.md)
- [docs/cybersec/E6_S1_CONTENT_CURATION.md](docs/cybersec/E6_S1_CONTENT_CURATION.md)
- [docs/cybersec/E6_S2_QUESTIONS_AND_SIMULATIONS.md](docs/cybersec/E6_S2_QUESTIONS_AND_SIMULATIONS.md)
- [docs/cybersec/E6_S3_ADAPTIVE_REVIEW_PATHS.md](docs/cybersec/E6_S3_ADAPTIVE_REVIEW_PATHS.md)
- [docs/roadmap/READINESS_REPORT_E0_E6.md](docs/roadmap/READINESS_REPORT_E0_E6.md)
- [docs/backlog/INITIAL_BACKLOG.md](docs/backlog/INITIAL_BACKLOG.md)

## Trilha de Estudos IA

O repositorio gerencia uma trilha de estudos sobre Inteligencia Artificial com 12 modulos:

| Deck | Tema |
|------|------|
| `IA::01 - Fundamentos` | Conceitos base, LLM, Prompt, Context, Skill, MCP, Agentes |
| `IA::02 - LLMs` | Arquitetura de Large Language Models |
| `IA::03 - Prompt Engineering` | Tecnicas avancadas de construcao de prompts |
| `IA::04 - Context Engineering` | Gerenciamento de contexto em interacoes |
| `IA::05 - Skills` | Procedimentos especializados reutilizaveis |
| `IA::06 - MCP` | Model Context Protocol e ferramentas |
| `IA::07 - RAG` | Retrieval-Augmented Generation |
| `IA::08 - Agentes` | Sistemas autonimos com IA |
| `IA::09 - Multiagentes` | Orquestracao de multiplos agentes |
| `IA::10 - DevOps IA` | CI/CD, MLflow, prompt versioning |
| `IA::11 - Arquiteturas` | Padroes de design para sistemas com IA |
| `IA::12 - Casos Reais` | Projetos praticos e estudos de caso |

### Importacao Inicial

Os 13 cards conceituais da trilha (todos em `IA::01 - Fundamentos`) estao em:

```
data/sources/ia/ia_fundamentos_cards.csv
```

Para importa-los no Anki (necessario Anki aberto com AnkiConnect instalado):

```bash
# Ativar ambiente virtual
source /home/suporte/Projetos/app_estudo/.venv/bin/activate

# Importar cards IA
python scripts/import_concurso_cards_to_anki.py \
    --mode ia \
    --csv data/sources/ia/ia_fundamentos_cards.csv \
    --report data/sources/ia/processed/ia_fundamentos_import_report.json
```

O comando e idempotente: na segunda execucao os cards existentes sao ignorados (skipped) e nenhuma duplicata e criada.

### Estrutura do CSV de Cards IA

```
card_id,front,back,deck,tags
CARD-IA-001,O que e um LLM?,Resposta...,IA::01 - Fundamentos,ia fundamentos llm
```

- `card_id`: identificador unico para deduplicacao
- `front`: texto da frente do card
- `back`: texto do verso (resposta/explicacao)
- `deck` (opcional): subdeck destino; padrao: `IA::01 - Fundamentos`
- `tags`: palavras-chave separadas por espaco

## Como Contribuir

Veja [CONTRIBUTING.md](CONTRIBUTING.md) e [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Smoke Test YouTube (E2.S4)

Instale dependencias Python e execute o smoke test da ingestao inicial de um video YouTube:

```bash
pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 /home/suporte/Projetos/app_estudo/.venv/bin/python scripts/smoke_youtube_ingestion.py \
	--url "https://www.youtube.com/watch?v=<VIDEO_ID>" \
	--title "Titulo do Video" \
	--db-path "data/audit/media_artifacts.db" \
	--languages "en"
```

Saida esperada: JSON com IDs dos artefatos gerados, quantidade de segmentos e status do gate de qualidade.

Para extrair audio junto no mesmo fluxo:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/suporte/Projetos/app_estudo/.venv/bin/python scripts/smoke_youtube_ingestion.py \
	--url "https://www.youtube.com/watch?v=<VIDEO_ID>" \
	--title "Titulo do Video" \
	--db-path "data/audit/media_artifacts.db" \
	--languages "en" \
	--extract-audio \
	--audio-output-dir "data/media/audio"
```

Sugestao de links iniciais por nivel em:
- [docs/english/YOUTUBE_STUDY_STARTER_LINKS.md](docs/english/YOUTUBE_STUDY_STARTER_LINKS.md)

Lote de videos para criar cards e sincronizar no Anki:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/suporte/Projetos/app_estudo/.venv/bin/python scripts/ingest_youtube_batch_to_anki.py \
	--batch-file "docs/english/YOUTUBE_STARTER_BATCH.json" \
	--db-path "data/audit/media_artifacts.db" \
	--endpoint "http://127.0.0.1:8765" \
	--model-name "AppEstudoListening" \
	--languages "en" \
	--extract-audio \
	--audio-output-dir "data/media/audio"
```

Observacao: abra o Anki com AnkiConnect ativo antes de executar o comando.

Arquivo pronto com 5 videos e fallback manual de transcript:
- [docs/english/YOUTUBE_BATCH_REAL_5.json](docs/english/YOUTUBE_BATCH_REAL_5.json)

Fallback manual por item no lote: se um video falhar no provider de transcript, inclua
`raw_text` (e opcionalmente `duration_seconds`, `raw_timestamps`, `locale`, `provider`)
no JSON para forcar ingestao manual daquele video sem interromper o lote inteiro.

Para aumentar a quantidade de cards por video, reduza a duracao alvo dos segmentos:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/suporte/Projetos/app_estudo/.venv/bin/python scripts/ingest_youtube_batch_to_anki.py \
	--batch-file "docs/english/YOUTUBE_STARTER_BATCH.json" \
	--target-segment-seconds 12 \
	--min-segment-seconds 8 \
	--max-segment-seconds 20
```

## Licenca

Este projeto esta sob a licenca MIT. Veja [LICENSE](LICENSE).

# Modelo de Entidades de Conhecimento Confiavel

## Objetivo

Definir entidades da frente E2.S5/E6.S4/E6.S5 com responsabilidades,
atributos principais, riscos, dependencias, observacoes futuras e relacoes.

## 1) SourceProvider

Responsabilidade:
- representar o provedor/origem institucional da fonte.

Atributos principais:
- provider_id;
- nome;
- tipo (institucional, comunitario, comercial, academico);
- dominio_oficial;
- pais;
- status.

Riscos:
- mudanca de politica publica sem aviso.

Dependencias:
- SourceGovernancePolicy.

Observacoes futuras:
- score historico de confiabilidade por provedor.

Relacoes:
- 1 SourceProvider -> N KnowledgeSource.

## 2) KnowledgeSource

Responsabilidade:
- unidade principal de cadastro de fonte para curadoria e uso por IA.

Atributos principais:
- source_id;
- provider_id;
- categoria/subcategoria;
- confiabilidade;
- idioma;
- formato;
- versao;
- status;
- reviewed_at;
- expires_at;
- maintainer.

Riscos:
- classificacao incorreta permitir automacao indevida.

Dependencias:
- SourceProvider, SourceGovernancePolicy.

Observacoes futuras:
- calibracao de confiabilidade por historico de erro.

Relacoes:
- N KnowledgeSource -> 1 SourceProvider;
- 1 KnowledgeSource -> 0..1 TrustedSource.

## 3) TrustedSource

Responsabilidade:
- representar fonte explicitamente aprovada para uso controlado.

Atributos principais:
- trusted_source_id;
- source_id;
- trust_level;
- ai_usage_policy;
- approval_version;
- approved_at;
- approved_by.

Riscos:
- manutencao desatualizada de status trusted.

Dependencias:
- KnowledgeSource, SourceGovernancePolicy.

Observacoes futuras:
- aprovacao automatica assistida por score de risco.

Relacoes:
- 1 TrustedSource -> 1 KnowledgeSource.

## 4) SourceGovernancePolicy

Responsabilidade:
- consolidar regras normativas para revisao, expiracao, versionamento e auditoria.

Atributos principais:
- policy_id;
- policy_version;
- review_cycle_days;
- expiration_rules;
- audit_event_schema;
- ai_permission_matrix;
- rollback_criteria.

Riscos:
- regras ambiguas gerarem decisoes inconsistentes.

Dependencias:
- governanca E0, rastreabilidade E3.

Observacoes futuras:
- assinatura digital de versoes de politica.

Relacoes:
- 1 SourceGovernancePolicy -> N KnowledgeSource.

## 5) KnowledgeNode

Responsabilidade:
- representar no de conhecimento para ontologia e RAG pedagogico.

Atributos principais:
- node_id;
- dominio;
- subdominio;
- conceito;
- prerequisitos;
- dificuldade;
- confiabilidade_media;
- status.

Riscos:
- semantica inconsistente entre dominios.

Dependencias:
- StudyTopic, Taxonomia E6.S5.

Observacoes futuras:
- embeddings e versao semantica auditavel.

Relacoes:
- N KnowledgeNode <-> N KnowledgeNode (depends_on/related_to).

## 6) CompetitionSource

Responsabilidade:
- modelar fonte de concurso por banca, edital e recorrencia.

Atributos principais:
- competition_source_id;
- banca;
- edital_ref;
- tipo_prova;
- estilo_textual;
- densidade_conceitual;
- pegadinhas;
- recorrencia_topicos;
- status.

Riscos:
- drift de perfil de banca ao longo do tempo.

Dependencias:
- KnowledgeSource, StudyTopic.

Observacoes futuras:
- score de aderencia por questao gerada.

Relacoes:
- 1 CompetitionSource -> N QuestionBlueprint.

## 7) StudyTopic

Responsabilidade:
- representar topico didatico alinhado a disciplina e objetivo.

Atributos principais:
- topic_id;
- disciplina;
- topico;
- objetivo;
- nivel;
- tags;
- status.

Riscos:
- granularidade inadequada para revisao adaptativa.

Dependencias:
- KnowledgeNode, QuestionBlueprint.

Observacoes futuras:
- curva de esquecimento por topico.

Relacoes:
- 1 StudyTopic -> N QuestionBlueprint.

## 8) QuestionBlueprint

Responsabilidade:
- definir contrato de geracao de questoes, simulados e cenarios.

Atributos principais:
- blueprint_id;
- topic_id;
- tipo_questao (conceitual, operacional, comparativa, troubleshooting, laboratorio);
- dificuldade;
- formato_banca;
- referencias;
- feedback_model;
- review_required.

Riscos:
- blueprint sem referencia confiavel gerar ruido pedagogico.

Dependencias:
- CompetitionSource, StudyTopic, TrustedSource.

Observacoes futuras:
- variantes por perfil de prova (Cebraspe, FGV, FCC, Cesgranrio, Vunesp).

Relacoes:
- N QuestionBlueprint -> 1 StudyTopic;
- N QuestionBlueprint -> 1..N CompetitionSource.

## 9) AdaptiveReviewProfile

Responsabilidade:
- modelar perfil adaptativo de revisao para perguntas e laboratorios.

Atributos principais:
- profile_id;
- learner_band;
- error_rate_thresholds;
- recurrence_thresholds;
- review_window_days;
- lab_recommendation_rules;
- status.

Riscos:
- limiares mal calibrados priorizarem topicos irrelevantes.

Dependencias:
- StudyTopic, QuestionBlueprint.

Observacoes futuras:
- recalibracao por desempenho longitudinal.

Relacoes:
- 1 AdaptiveReviewProfile -> N StudyTopic;
- 1 AdaptiveReviewProfile -> N QuestionBlueprint.

## Rastreabilidade

- Etapa/Subetapa: E2.S5, E6.S4, E6.S5
- Backlog: BLG-0041, BLG-0042, BLG-0043

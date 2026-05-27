# E2.S4 - Ingestao e Processamento de Midia

## Contexto

A etapa E2 foi concluida em E2.S1-E2.S3 para curadoria, avaliacao e validacao de transcricao.
E2.S4 expande a arquitetura para formalizar ingestao e processamento de midia sem regressao
nos artefatos existentes.

## Objetivo

Definir arquitetura, fluxo, modelagem e governanca para transformar conteudo bruto de midia
em itens curados prontos para avaliacao e sincronizacao logica com Anki.

## Escopo

- pipeline de ingestao, extracao, normalizacao, segmentacao e persistencia;
- YouTube como primeira fonte oficial de ingestao;
- separacao formal entre conteudo bruto e conteudo curado;
- politica de versionamento e reprocessamento;
- rastreabilidade de origem e lineage raw -> curated.

## Fora do escopo

- implementacao de codigo;
- automacao de pipeline em runtime;
- scripts operacionais;
- integracao tecnica de baixo nivel com APIs externas.

## Pipeline de referencia

```txt
Source Media
  -> Extraction
  -> Transcript Validation
  -> Normalization
  -> Segmentation
  -> Curated Study Item
  -> Evaluation
  -> Logical Anki Note
  -> Sync Pipeline
```

## Fonte oficial inicial

YouTube e a primeira fonte oficial de ingestao e deve ter:

- identificador externo obrigatorio (`platform=YouTube`, `external_id`);
- URL canonica e URL de captura;
- timestamps de criacao, captura e ultima verificacao;
- evidencia da origem (canal, titulo, idioma, duracao);
- hash de referencia para detectar alteracoes na origem.

Regra complementar de governanca:
- YouTube e fonte primaria audiovisual, mas nao e automaticamente confiavel;
- toda entrada deve passar por curadoria e classificacao de confiabilidade antes de uso por IA.

## Entidades arquiteturais

### 1) SourceMedia

Responsabilidade:
- representar a origem de midia antes de qualquer curadoria textual.

Atributos principais:
- `source_media_id`;
- `platform`;
- `external_id`;
- `canonical_url`;
- `media_type`;
- `language`;
- `duration_seconds`;
- `created_at`, `captured_at`, `last_seen_at`;
- `source_hash`.

Vinculos:
- 1 SourceMedia -> N RawTranscript;
- 1 SourceMedia -> N SourceMetadata.

Riscos:
- remocao ou edicao da fonte externa;
- colisao de URLs para o mesmo conteudo.

Evolucao futura:
- suportar multiplas plataformas mantendo contrato unico de origem.

### 2) RawTranscript

Responsabilidade:
- armazenar transcricao bruta sem normalizacao semantica.

Atributos principais:
- `raw_transcript_id`;
- `source_media_id`;
- `provider`;
- `raw_text`;
- `raw_timestamps`;
- `locale`;
- `ingestion_version`;
- `content_hash`;
- `captured_at`.

Vinculos:
- N RawTranscript -> 1 SourceMedia;
- 1 RawTranscript -> N NormalizedSentence.

Riscos:
- ruido alto, lacunas e baixa confiabilidade temporal.

Evolucao futura:
- registrar proveniencia por trecho para reconciliacao de multiplos provedores.

### 3) CuratedTranscript

Responsabilidade:
- consolidar versao curada da transcricao aprovada para estudo.

Atributos principais:
- `curated_transcript_id`;
- `source_media_id`;
- `raw_transcript_id`;
- `curated_text`;
- `curation_status`;
- `curation_notes`;
- `quality_score`;
- `curated_version`;
- `approved_at`.

Vinculos:
- 1 CuratedTranscript -> N StudySegment;
- 1 CuratedTranscript -> N NormalizedSentence.

Riscos:
- sobre-normalizacao que descaracteriza fala natural.

Evolucao futura:
- manter variantes de curadoria por nivel (A2, B1, B2).

### 4) StudySegment

Responsabilidade:
- representar recorte pedagogico reutilizavel para treino e revisao.

Atributos principais:
- `study_segment_id`;
- `curated_transcript_id`;
- `segment_start_ms`, `segment_end_ms`;
- `segment_text`;
- `pedagogical_unit`;
- `difficulty_band`;
- `segment_hash`.

Vinculos:
- N StudySegment -> 1 CuratedTranscript;
- 1 StudySegment -> N CuratedStudyItem.

Riscos:
- segmentos longos demais reduzindo foco didatico.

Evolucao futura:
- estrategia adaptativa de tamanho de segmento por proficiencia.

### 5) NormalizedSentence

Responsabilidade:
- armazenar sentencas normalizadas com trilha de transformacao.

Atributos principais:
- `normalized_sentence_id`;
- `raw_transcript_id`;
- `curated_transcript_id` (opcional);
- `sentence_index`;
- `raw_sentence`;
- `normalized_sentence`;
- `normalization_flags`;
- `normalization_version`.

Vinculos:
- N NormalizedSentence -> 1 RawTranscript;
- N NormalizedSentence -> 0..1 CuratedTranscript.

Riscos:
- perda de marcas de oralidade relevantes para listening.

Evolucao futura:
- politicas distintas de normalizacao por objetivo pedagogico.

### 6) SourceMetadata

Responsabilidade:
- registrar metadados de curadoria e classificacao da fonte.

Atributos principais:
- `source_metadata_id`;
- `source_media_id`;
- `accent_profile`;
- `speech_rate_profile`;
- `subtitle_type`;
- `transcript_quality`;
- `connected_speech_density`;
- `noise_level`;
- `pedagogical_category`;
- `context_tags`.

Vinculos:
- N SourceMetadata -> 1 SourceMedia.

Riscos:
- classificacao subjetiva sem calibracao entre curadores.

Evolucao futura:
- calibracao interavaliador e score composto por consenso.

## Curadoria de fontes (criterios obrigatorios)

- sotaque;
- velocidade;
- clareza;
- naturalidade;
- tipo de legenda;
- qualidade da transcricao;
- densidade de connected speech;
- ruido;
- contexto;
- categoria pedagogica.

## Tipos de midia

Taxonomia inicial para classificacao da origem:

- podcast;
- entrevista;
- TED Talk;
- serie;
- filme;
- gameplay;
- documentario;
- aula;
- noticia;
- vlog;
- conversa espontanea.

## Estrategia de segmentacao (chunking)

Regra base:
- nao usar 1 video = 1 card.

Granularidades formais:
- video: unidade de origem e auditoria;
- segmento: recorte temporal com objetivo didatico;
- frase: unidade linguistica para normalizacao e avaliacao de ruptura;
- unidade pedagogica: agrupamento de frases/segmentos por habilidade alvo.

Diretrizes:
- segmento recomendado entre 10 e 45 segundos para treino ativo;
- quebra por mudanca de topico, pausa longa ou densidade de ruido;
- preservar contexto minimo para evitar frases isoladas sem significado.

## Pipeline de normalizacao textual

Etapas:

1. limpeza de timestamps fora do campo temporal dedicado;
2. tratamento de contractions sem apagar formas naturais relevantes;
3. remocao de fillers nao pedagogicos (com flag de auditoria);
4. remocao de ruido textual e duplicidades;
5. normalizacao de espacos e caracteres especiais;
6. marcacao de sentencas incompletas para revisao;
7. emissao de versao normalizada com hash e versao de regra.

## Persistencia de midia e metadados

Campos minimos de persistencia:

- URLs (canonica e de captura);
- IDs externos;
- timestamps de origem e processamento;
- transcricoes brutas e curadas;
- versoes de processamento;
- hashes por artefato;
- referencias de audio/video;
- status de curadoria.

Regra de separacao:
- conteudo bruto e conteudo curado devem permanecer em entidades separadas para manter
  auditabilidade e rollback documental.

## Politica de versionamento

- atualizacao: nova observacao da mesma origem com mesmo `external_id` e hash diferente;
- substituicao: nova versao curada invalida versao anterior para uso pedagogico;
- reconciliacao: mesclar divergencias de metadados preservando historico;
- invalidacao: marcar artefato nao confiavel sem apagar evidencia historica;
- reprocessamento: reexecutar pipeline com nova versao de regra mantendo lineage.

## Riscos e dependencias

Dependencias:
- E2.S1 (curadoria de fonte);
- E2.S2 (matriz de avaliacao);
- E2.S3 (validacao de transcricao);
- E2.S5 (governanca e curadoria de fontes);
- E3.S1-E3.S3 (entidades, vinculos e auditoria);
- E4.S1-E4.S2 (consumo por nota logica/sync).

Riscos principais:
- variabilidade de qualidade de transcricao em fonte aberta;
- acoplamento excessivo entre normalizacao e segmentacao;
- perda de lineage se raw/curated nao forem separados;
- drift de classificacao de curadoria sem politica de calibracao.

Mitigacoes documentais:
- contrato de entidade com atributos obrigatorios;
- hash/versionamento em todos os artefatos textuais;
- gates de transicao com evidencias minimas;
- checklist de lineage em auditoria de lote.

## Rastreabilidade

- Etapa/Subetapa: E2.S4
- Backlog: BLG-0023, BLG-0024, BLG-0025, BLG-0026, BLG-0027, BLG-0028, BLG-0029
- Dependencias: BLG-0007, BLG-0008, BLG-0009, BLG-0012, BLG-0013, BLG-0014, BLG-0015

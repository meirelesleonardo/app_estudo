# Governanca do Projeto

## Objetivo

Padronizar como o projeto evolui, documenta decisoes e garante consistencia.

## Convencoes de nomenclatura

### Etapas e subetapas
- Etapa: E0, E1, E2...
- Subetapa: E1.S1, E1.S2...

### Backlog
- Item: BLG-0001, BLG-0002...

### Decisoes
- ADR: ADR-0001, ADR-0002...

### SPECs
- SPEC: SPEC-E1-S1-001

## Estrategia de branch

- main: historico estavel e documentacao validada.
- docs/<tema-curto>: alteracoes documentais.
- planning/<etapa>: refinamentos de etapa.
- spec/<id-spec>: preparacao de especificacoes aprovadas.

## Convencao de commits

Padrao sugerido:
- docs: atualiza curadoria de fontes E2
- roadmap: reprioriza backlog de E1
- governance: adiciona regra de branch
- trace: vincula BLG-0008 a E2.S2

## Versionamento

Durante fase documental:
- usar tags de marco, exemplo: v0.1-doc-foundation.

Quando houver codigo:
- adotar SemVer.

## Changelog

- manter registro em CHANGELOG.md;
- agrupar por Added, Changed, Deprecated, Removed, Fixed.

## Politica de decisoes arquiteturais

Toda decisao relevante deve:
- virar ADR;
- indicar contexto e alternativas;
- declarar impactos e trade-offs;
- apontar itens de backlog afetados.

## Trusted Knowledge Sources e Knowledge Governance

Principios obrigatorios:
- IA so pode operar sobre fontes aprovadas, rastreaveis, classificadas, auditaveis e versionadas;
- nenhuma fonte comunitaria ou experimental entra em automacao sem curadoria formal;
- toda fonte deve ter dono (mantenedor), data de revisao e data de expiracao.

Classificacao oficial de fonte:
- oficial;
- normativa;
- operacional;
- pedagogica;
- comunitaria;
- experimental;
- laboratorio;
- audiovisual;
- documental.

Niveis de confiabilidade:
- alta;
- media;
- baixa;
- experimental.

Atributos minimos de governanca por fonte:
- source_id unico;
- categoria e subcategoria;
- nivel de confiabilidade;
- origem oficial;
- data de revisao e data de expiracao;
- idioma e formato;
- estrategia de uso por IA;
- risco e observacoes;
- status e versao;
- mantenedor responsavel.

Politica de uso pela IA:
- card automatico: somente fonte oficial/normativa/pedagogica com confiabilidade alta e curadoria aprovada;
- card com revisao humana: fonte operacional/comunitaria ou confiabilidade media;
- simulados: fonte normativa, oficial e banco historico curado por banca;
- laboratorios: fonte operacional e laboratorio com checklist de seguranca e evidencia;
- proibido sem validacao: fonte experimental, baixa confiabilidade, expirada ou sem mantenedor.

## Definicao de pronto (documental)

Um item documental esta pronto quando:
- possui objetivo claro;
- possui criterio de conclusao;
- possui links para etapa e backlog;
- possui revisao minima de consistencia.

## Definicao de pronto para implementacao

Uma etapa so pode iniciar codigo se:
- refinamento e subetapas concluidos;
- SPEC aprovada;
- riscos principais mitigados;
- metricas de sucesso definidas.

## Lifecycle documental e operacional

Estados oficiais de lifecycle:
- Draft;
- Refining;
- Approved;
- Implementing;
- Validating;
- Operational;
- Deprecated.

Criterios de transicao (resumo):
- Draft -> Refining: escopo inicial registrado com etapa/subetapa e backlog vinculado.
- Refining -> Approved: criterios de conclusao definidos, dependencias declaradas e riscos explicitados.
- Approved -> Implementing: gate pre-SPEC aprovado e checklist de pronto para implementacao atendido.
- Implementing -> Validating: evidencia minima de entrega produzida (doc/testes/artefato conforme tipo).
- Validating -> Operational: criterios de aceite atendidos e rastreabilidade atualizada.
- Operational -> Deprecated: substituicao formal aprovada com ADR ou decisao equivalente.

Criterio de rollback (obrigatorio):
- qualquer estado pode retroceder para o estado anterior quando houver risco nao mitigado,
  evidencia inconsistente ou quebra de rastreabilidade;
- rollback deve registrar motivo, impacto e plano corretivo no mesmo ciclo documental;
- rollback de Operational exige referencia explicita de substituicao ou congelamento controlado.

Gates minimos por estado:
- gate de definicao: objetivo, escopo e fora de escopo claros;
- gate de rastreabilidade: vinculo Etapa/Subetapa/Backlog e impactos declarados;
- gate de risco: riscos e mitigacoes documentados;
- gate de evidencia: criterio observavel de conclusao e evidencia verificavel.

Evidencias obrigatorias:
- link para backlog;
- link para artefato principal (doc/SPEC/ADR);
- criterio de conclusao observavel;
- registro de dependencia e impacto.

Evidencias adicionais para Knowledge Governance:
- classificacao de fonte e nivel de confiabilidade registrados;
- data de revisao e expiracao preenchidas;
- politica de uso por IA declarada (automatico, revisao humana, proibido);
- status de curadoria e versao rastreaveis.

# Politica de Curadoria YouTube (Fonte Audiovisual Primaria)

## Objetivo

Formalizar YouTube como fonte primaria audiovisual com governanca,
sem assumir confiabilidade automatica.

## Principio

- YouTube e fonte primaria audiovisual;
- YouTube nao e automaticamente fonte confiavel;
- todo conteudo exige curadoria antes de uso por IA.

## Pipeline de curadoria

1. Ingestao inicial com metadata obrigatoria.
2. Validacao de legenda/transcricao.
3. Classificacao de qualidade audiovisual e pedagogica.
4. Aprovacao ou bloqueio para consumo por IA.

## Criterios obrigatorios de avaliacao

- qualidade de legenda;
- naturalidade da fala;
- densidade pedagogica;
- ruido;
- velocidade;
- sotaque.

## Escala de classificacao sugerida

- Aprovado: apto para uso com politica definida;
- Revisao humana: uso restrito;
- Bloqueado: proibido para automacao.

## Rastreabilidade de midia

Campos obrigatorios:
- source_id;
- external_id;
- timestamps (captura/processamento/revisao);
- hashes de referencia;
- metadata persistente;
- versao de transcricao;
- origem da legenda;
- status de curadoria.

## Rastreabilidade

- Etapa/Subetapa: E2.S5
- Backlog: BLG-0038

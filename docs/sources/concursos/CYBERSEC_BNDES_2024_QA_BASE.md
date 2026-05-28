# BNDES 2024 - Prova 2 Ciberseguranca - Base Q&A (Preliminar)

## Objetivo

Registrar a base inicial de questoes objetivas com respostas corretas,
com rastreabilidade de origem e status de curadoria.

## Arquivos de origem

- data/sources/concursos/raw/prova_cibersegurança.pdf
- data/sources/concursos/raw/Gabarito_Final.pdf

## Arquivos gerados

- data/sources/concursos/processed/bndes_2024_prova2_objetiva_q1_q70.json
- data/sources/concursos/processed/bndes_2024_prova2_objetiva_q1_q70_enriched.json
- data/sources/concursos/processed/bndes_2024_prova2_cards_seed.csv

## Cobertura atual

- respostas corretas mapeadas: 70/70 (conforme gabarito final, Prova 2);
- enunciados/alternativas: extraidos automaticamente e pendentes de revisao final;
- status geral: ready_for_review.

## Risco conhecido

A extração textual de PDF em duas colunas pode causar:
- quebra de linhas em locais indevidos;
- contaminacao de enunciado com elementos de pagina;
- necessidade de validacao manual antes de sincronizar no Anki.

## Regra de uso

Nao enviar automaticamente ao Anki sem revisao humana de consistencia
(enunciado, alternativas e aderencia prova-gabarito).

## Proximo passo operacional

1. Revisar questao a questao no JSON enriquecido.
2. Marcar status_curadoria=approved apenas quando validada.
3. Gerar lote final de cards para sync.

## Rastreabilidade

- Etapa/Subetapa: E2.S5, E6.S4
- Backlog: BLG-0040, BLG-0041

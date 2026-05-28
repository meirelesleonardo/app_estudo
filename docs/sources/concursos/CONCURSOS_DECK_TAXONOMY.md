# Taxonomia de Decks - Concursos

## Objetivo

Padronizar a estrutura de decks para permitir estudo continuo no mesmo dia,
com foco por materia/submateria e escalabilidade para novos dominios
(Portugues, Direito, Ciberseguranca e outros).

## Problema observado

Quando todo o lote fica em um unico deck final, os limites diarios de estudo
podem bloquear continuidade no mesmo dia. Com subdecks por materia/submateria,
e possivel alternar trilhas sem perder foco pedagogico.

## Padrao recomendado

### Tronco por projeto/prova

- Concursos::<Orgao>::<Area>::Materias

Exemplo atual:

- Concursos::BNDES::Ciberseguranca::Materias

### Folhas por materia e submateria

- Concursos::<Orgao>::<Area>::Materias::<Materia>::<Submateria>

Exemplos:

- Concursos::BNDES::Ciberseguranca::Materias::Economia::Politica_Publica
- Concursos::BNDES::Ciberseguranca::Materias::Portugues::interpretacao_e_gramatica
- Concursos::BNDES::Ciberseguranca::Materias::IAM_e_Controle_de_Acesso::Geral

## Regra de roteamento a partir do campo Topic

Entrada no campo Topic:

- "Materia/Submateria" -> Materia + Submateria
- "Materia - Submateria" -> Materia + Submateria
- "Materia" -> Materia + Geral
- vazio -> SemTopico + SemSubtopico

Normalizacao de nomes:

- remocao de acentos;
- caracteres nao alfanumericos convertidos para underscore;
- espacos colapsados;
- remocao de underscores duplicados.

## Fluxo operacional recomendado

1. Importar novos cards diretamente por topico no tronco Materias.
2. Estudar no deck pai quando quiser fila continua no dia.
3. Estudar no subdeck folha quando quiser foco por materia.
4. Ajustar limites diarios no preset do Anki para evitar bloqueio precoce.

## Comando de importacao por topico

Use o script de importacao com --deck-by-topic-root:

/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/import_concurso_cards_to_anki.py \
  --csv data/sources/concursos/processed/bndes_2024_prova2_cards_enhanced.csv \
  --deck-by-topic-root "Concursos::BNDES::Ciberseguranca::Materias" \
  --report data/sources/concursos/processed/bndes_2024_prova2_anki_import_by_topic_report.json

## Expansao futura recomendada

Para manter padrao unico entre concursos gerais e tecnicos:

- Concursos::Base::Portugues::...
- Concursos::Base::Direito::...
- Concursos::Tecnico::Ciberseguranca::...
- Concursos::Tecnico::Redes::...

Ou por edital/orgao, quando o estudo for direcionado:

- Concursos::<Orgao>::Base::Portugues::...
- Concursos::<Orgao>::Base::Direito::...
- Concursos::<Orgao>::Tecnico::Ciberseguranca::...

## Observacao

A contagem em deck pai no Anki e acumulada (soma dos filhos). Para medir
progresso por trilha, observar subdecks folha.

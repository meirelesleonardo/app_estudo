# Checklist de Extracao - Provas Cybersec

## Objetivo

Garantir extracao consistente de questoes e gabarito antes da etapa de criacao de cards.

## Etapa 1 - Validar arquivos

- [x] Confirmar os 3 PDFs disponiveis no workspace.
- [x] Identificar quais sao provas e qual e gabarito.
- [x] Registrar nome exato dos arquivos no inventario.

## Etapa 2 - Validar correspondencia prova-gabarito

- [x] Ler cabecalho/codigo de prova.
- [x] Validar se o gabarito referencia a mesma versao da prova.
- [x] Registrar regra de correspondencia usada.
- [x] Marcar nivel de confianca da correspondencia.

## Etapa 3 - Extrair questoes

- [x] Extrair numero e enunciado de cada questao.
- [x] Extrair alternativas completas.
- [x] Extrair resposta correta pelo gabarito correspondente.
- [x] Registrar pagina de evidencia.

## Etapa 4 - Curadoria pedagogica

- [x] Classificar assunto e subassunto.
- [x] Identificar habilidade cobrada.
- [x] Escrever explicacao direta da resposta.
- [x] Escrever explicacao aprofundada (contexto de prova e tecnico).
- [x] Citar fontes confiaveis.

## Etapa 5 - Pronto para card

- [x] exam_question_id unico definido.
- [x] resposta correta validada.
- [x] explicacao revisada.
- [x] tags de assunto/subassunto definidas.
- [x] status_curadoria = approved.

## Etapa 6 - Sincronizacao no Anki

- [x] Validar conectividade com AnkiConnect.
- [x] Criar deck e modelo de nota dedicados para concurso.
- [x] Importar lote final revisado.
- [x] Confirmar quantidade de cards no deck apos importacao.

## Etapa 7 - Reforco Pedagogico

- [x] Atualizar deck principal com explicacoes aprofundadas e analise de alternativas incorretas.
- [x] Criar deck tecnico focado (Q36-Q70) para treino de ciberseguranca.
- [x] Validar quantidade final dos decks: Prova2 (70) e Tecnico_Q36_70 (35).

## Etapa 8 - Taxonomia de Decks e Escalabilidade

- [x] Reorganizar cards da Prova2 por materia/submateria no tronco Materias.
- [x] Preparar taxonomia padrao para expansao futura (Portugues, Direito e Tecnico).
- [x] Habilitar importacao com roteamento automatico por Topic para novos lotes.

## Observacao importante

Sem os PDFs no workspace, a extracao nao pode ser iniciada.

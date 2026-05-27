# E6.S3 - Trilhas Adaptativas de Revisao e Laboratorios

## Objetivo

Definir regras de adaptatividade para priorizar revisao de topicos criticos e orientar laboratorios praticos.

## Modelo de adaptatividade

Entradas:
- desempenho por disciplina;
- recorrencia de erros por topico;
- tempo de resposta;
- historico recente de simulados.

Saidas:
- priorizacao de topicos de revisao;
- recomendacao de bloco de questoes;
- sugestao de laboratorio pratico direcionado.

## Politica de priorizacao

- erro alto + recorrencia alta = prioridade imediata;
- erro medio + tendencia de melhora = revisao moderada;
- erro baixo + estabilidade = manutencao.

## Trilhas sugeridas

- trilha de recuperacao (lacunas fundamentais);
- trilha de consolidacao (topicos em progresso);
- trilha de aperfeicoamento (nivel avancado).

## Laboratorios (visao inicial)

- analise de incidentes simulados;
- triagem de logs e eventos;
- controles e hardening basicos;
- exercicios guiados por cenario.

## Criterios de sucesso

- reducao de erro recorrente por topico;
- aumento de estabilidade em simulados consecutivos;
- melhoria de tempo medio sem perda de acuracia.

## Pendencias para fechamento de S3

- definir limiares quantitativos de troca de trilha;
- definir catalogo inicial de laboratorios por disciplina;
- definir janela de reavaliacao adaptativa.

## Rastreabilidade

- Etapa/Subetapa: E6.S3
- Backlog: BLG-0022

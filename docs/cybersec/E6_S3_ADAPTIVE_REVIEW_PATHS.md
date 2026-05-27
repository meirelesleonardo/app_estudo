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

## Limiares quantitativos de troca de trilha (definidos)

- Recuperacao:
	erro por topico >= 35% ou acuracia da disciplina < 60%.

- Consolidacao:
	erro por topico entre 15% e 34% e acuracia entre 60% e 79%.

- Aperfeicoamento:
	erro por topico < 15% e acuracia >= 80% por 2 ciclos consecutivos.

## Janela de reavaliacao adaptativa (definida)

- reavaliacao curta: a cada 7 dias para trilha de recuperacao;
- reavaliacao padrao: a cada 14 dias para consolidacao;
- reavaliacao de manutencao: a cada 21 dias para aperfeicoamento.

## Catalogo inicial de laboratorios por disciplina (definido)

1. Seguranca da informacao
- laboratorio de classificacao de controles por risco.

2. Redes e protocolos
- laboratorio de analise de trafego e identificacao de anomalias.

3. Criptografia aplicada
- laboratorio de escolha de mecanismos criptograficos por cenario.

4. Gestao de riscos e normas
- laboratorio de mapeamento de controles para frameworks.

5. Resposta a incidentes
- laboratorio de triagem, contencao e plano de resposta.

6. Legislacao e governanca publica
- laboratorio de enquadramento de cenario em requisitos normativos.

## Fechamento de S3

- limiares de troca de trilha definidos;
- catalogo inicial de laboratorios publicado;
- janela de reavaliacao adaptativa definida.

## Rastreabilidade

- Etapa/Subetapa: E6.S3
- Backlog: BLG-0022

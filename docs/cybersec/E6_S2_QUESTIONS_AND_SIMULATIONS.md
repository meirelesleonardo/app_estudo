# E6.S2 - Estrategia de Questoes e Simulados

## Objetivo

Definir o modelo de elaboracao, classificacao e uso de questoes para revisao e simulacao de concursos.

## Blueprint de questoes

Cada questao deve possuir:
- id rastreavel;
- disciplina e topico;
- nivel de dificuldade;
- tipo (conceitual, aplicacao, cenario, normativa);
- justificativa e referencia;
- vinculo com objetivo de estudo.

## Blueprint de simulados

- composicao equilibrada por disciplina;
- distribuicao de dificuldade;
- tempo alvo por bloco;
- criterio de correcao e feedback.

## Regras de qualidade

- questao deve mapear um objetivo claro;
- enunciado sem ambiguidade desnecessaria;
- feedback com explicacao objetiva;
- historico de versoes quando houver ajuste.

## Estrategia de uso

- ciclos curtos de questoes por topico;
- simulados parciais por area;
- simulados completos por marco de progresso.

## Metricas sugeridas

- acuracia por disciplina;
- tempo medio por questao;
- taxa de recorrencia de erro por topico;
- evolucao de desempenho entre simulados.

## Matriz inicial de distribuicao de questoes (definida)

### Simulado parcial (30 questoes)

- Seguranca da informacao: 6
- Redes e protocolos: 6
- Criptografia aplicada: 5
- Gestao de riscos e normas: 5
- Resposta a incidentes: 5
- Legislacao e governanca publica: 3

Distribuicao de dificuldade:
- basico: 40%
- intermediario: 40%
- avancado: 20%

### Simulado completo (80 questoes)

- Seguranca da informacao: 16
- Redes e protocolos: 16
- Criptografia aplicada: 14
- Gestao de riscos e normas: 12
- Resposta a incidentes: 14
- Legislacao e governanca publica: 8

Distribuicao de dificuldade:
- basico: 30%
- intermediario: 45%
- avancado: 25%

## Regra de construcao de simulados (definida)

1. Nenhum simulado pode ter disciplina com menos de 10% de cobertura.
2. Simulado parcial deve priorizar topicos de maior recorrencia de erro.
3. Simulado completo deve manter distribuicao balanceada por disciplina.
4. Duas aplicacoes consecutivas nao devem repetir mais de 25% das questoes.

## Padrao de feedback por erro (definido)

Cada erro deve retornar:
- causa principal;
- referencia de estudo;
- topico para revisao imediata;
- nivel de urgencia (alta, media, baixa).

## Fechamento de S2

- matriz inicial de distribuicao publicada;
- regra de construcao de simulados publicada;
- padrao de feedback por erro definido.

## Rastreabilidade

- Etapa/Subetapa: E6.S2
- Backlog: BLG-0021

## Expansao incremental vinculada

Este artefato e base para:
- E6.S4 (motor inteligente de questoes);
- E6.S5 (taxonomia e ontologia para cobertura semantica por topico e banca).

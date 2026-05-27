# E6.S4 - Motor Inteligente de Questoes

## Contexto

S4 expande E6.S2 e E6.S3 para habilitar geracao e revisao adaptativa de questoes,
sem iniciar implementacao tecnica e sem regressao do modulo de ingles.

## Objetivo

Formalizar arquitetura do motor inteligente para:
- geracao adaptativa;
- revisao adaptativa;
- simulados;
- cenarios tecnicos;
- questoes conceituais;
- questoes operacionais;
- questoes comparativas;
- troubleshooting;
- laboratorios.

## Escopo

- contrato de QuestionBlueprint e perfil adaptativo;
- matriz de tipos de questao por dominio;
- regras de uso por banca e recorrencia;
- gates de qualidade para entrada no ciclo de simulados.

## Fora do escopo

- implementacao de gerador automatico;
- consumo de APIs externas;
- execucao automatizada de laboratorios.

## Tipos de questao (contrato)

- conceitual;
- operacional;
- comparativa;
- troubleshooting;
- laboratorio guiado;
- cenario tecnico contextual.

## Matriz de aplicacao por banca

Bancas prioritarias:
- Cebraspe;
- FGV;
- FCC;
- Cesgranrio;
- Vunesp.

Atributos por banca:
- estilo textual;
- densidade conceitual;
- pegadinhas recorrentes;
- formato de resposta;
- recorrencia de topicos.

## Regras de uso por IA

- geracao automatica so para blueprints com fonte trusted;
- blueprints com fonte media exigem revisao humana;
- blueprints experimentais ficam bloqueados para simulado oficial.

## Riscos

- drift de estilo de banca sem recalibracao;
- geracao de questao sem base confiavel;
- superenfase em topicos de alta recorrencia sem cobertura equilibrada.

## Dependencias

- E2.S5 (governanca de fontes);
- E6.S1 (curadoria por edital e disciplina);
- E6.S2 (blueprint de simulados);
- E6.S3 (adaptatividade e laboratorios).

## Rastreabilidade

- Etapa/Subetapa: E6.S4
- Backlog: BLG-0041, BLG-0043

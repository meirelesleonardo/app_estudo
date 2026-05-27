# Arquitetura Macro do Projeto

## Contexto

O projeto nasce como plataforma documental e evolutiva para automacao de estudos com IA. A implementacao sera posterior e orientada por etapas refinadas.

## Objetivo

Definir os blocos arquiteturais principais, seus limites e relacoes para guiar o crescimento incremental.

## Escopo

- visao de modulos;
- fronteiras funcionais;
- fluxo macro de evolucao;
- dependencias entre blocos.

## Fora de escopo

- design de API;
- modelagem de banco definitiva;
- implementacao de scripts e servicos.

## Blocos Arquiteturais

1. Camada de Curadoria de Conteudo
- selecao e qualificacao de fontes;
- classificacao por dificuldade e naturalidade;
- controle de qualidade de transcricao.

2. Camada de Estrategia Pedagogica
- trilhas de listening por nivel;
- ciclos ouvir-entender-conferir-repetir;
- politicas de revisao espacada.

3. Camada de Inteligencia (futura)
- geracao assistida de cards e exercicios;
- ajuste de dificuldade por desempenho;
- sugestao de conteudo adaptativo.

4. Camada de Integracao Anki (futura)
- mapeamento de nota/deck/tag;
- envio e atualizacao de cards;
- sincronizacao de midia.

5. Camada de Rastreamento e Governanca
- IDs de etapa/subetapa/artefato;
- historico de decisoes;
- trilha de evolucao e auditoria.

## Dependencias Macro

- Curadoria valida e pre-requisito para estrategia pedagogica.
- Estrategia pedagogica define requisitos para IA e Anki.
- Rastreamento e governanca sao transversais desde o inicio.

## Riscos

- iniciar implementacao sem refinamento documental;
- aumentar escopo antes de consolidar modulo de ingles;
- perda de contexto entre conversas sem padrao de continuidade.

## Metricas de maturidade arquitetural

- percentual de etapas com escopo e nao escopo definidos;
- percentual de backlog com rastreabilidade completa;
- quantidade de decisoes registradas em ADR;
- estabilidade dos criterios de avaliacao de fontes.

## Entregaveis desta fase

- mapa de blocos arquiteturais;
- dependencias entre etapas;
- criterio de evolucao arquitetural incremental.

## Proximos passos

- consolidar refinamento E1 e E2;
- formalizar arquitetura de rastreabilidade em detalhe;
- preparar artefatos para futura especificacao tecnica.

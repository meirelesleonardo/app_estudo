# E5.S1 - Escopo Minimo do MVP Implementavel

## Objetivo

Definir o menor recorte implementavel que valide o fluxo central do projeto sem expandir prematuramente o escopo.

## Problema que o MVP resolve

Permitir ciclo basico de estudo de listening com curadoria e estrutura pronta para futura sincronizacao com Anki, mantendo rastreabilidade ponta a ponta.

## Escopo minimo (incluso)

- ingestao documental de item curado de listening;
- classificacao por nivel e fenomeno (connected speech, contracoes, reducao);
- aplicacao da matriz de avaliacao de listening;
- mapeamento logico para nota/deck/tag conforme E4;
- registro de status e historico no modelo de rastreabilidade.

## Fora do escopo (explicitamente)

- automacao completa de pipelines;
- dashboard web;
- recomendacao adaptativa por IA em producao;
- suporte multi-modulo (concursos/cybersec) no primeiro ciclo;
- sincronizacao em massa com alto volume.

## Entradas do MVP

- fonte curada validada;
- metadados minimos de dificuldade e sotaque;
- trecho de transcricao confiavel;
- classificacao pedagogica (nivel, habilidade, fenomeno).

## Saidas esperadas

- item de estudo estruturado e rastreavel;
- representacao logica de nota pronta para futura sincronizacao;
- evidencia documental de qualidade e status.

## Criterios de sucesso do MVP

- completude de rastreabilidade por item >= 95%;
- duplicidade logica <= 2% nos itens avaliados;
- classificacao pedagogica preenchida em 100% dos itens do lote piloto;
- conformidade com gate pre-SPEC para todo incremento planejado.

## Dependencias

- E1 concluida;
- E2 concluida;
- E3 concluida;
- E4 concluida.

## Riscos

- tentar incluir funcionalidades avancadas antes de validar fluxo minimo;
- backlog tecnico amplo sem priorizacao por valor;
- falta de criterio objetivo para declarar pronto para implementacao.

## Rastreabilidade

- Etapa/Subetapa: E5.S1
- Backlog: BLG-0011

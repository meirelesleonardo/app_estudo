# E4.S3 - Tratamento de Excecoes e Divergencias

## Objetivo

Definir como a futura integracao deve reagir a falhas, inconsistencias e conflitos sem perder rastreabilidade.

## Pre-requisitos

- modelo logico e fluxos de sincronizacao definidos (E4.S1 e E4.S2);
- estrategia de rastreabilidade de E3 ativa;
- taxonomia inicial de tags documentada.

## Passos

### 1. Classificar excecoes

## Classes de excecao

### 1. Excecoes de conectividade

- AnkiConnect indisponivel;
- timeout de operacao;
- resposta incompleta.

Resposta esperada:
- registrar falha;
- manter item em estado reprocessavel;
- nao marcar sincronizacao como concluida.

### 2. Excecoes de integridade de dados

- nota sem campo obrigatorio;
- tag fora da taxonomia;
- deck inexistente;
- midia sem referencia valida.

Resposta esperada:
- bloquear envio;
- registrar motivo objetivo;
- encaminhar para correcao documental ou tecnica.

### 3. Excecoes de duplicidade e conflito

- nota ja existente com mesmo identificador;
- divergencia entre fonte curada e nota sincronizada;
- ambiguidade de vinculacao de midia.

Resposta esperada:
- marcar estado conflict;
- impedir merge silencioso;
- exigir politica de reconciliacao.

### 4. Excecoes de evolucao de modelo

- mudanca futura de campos;
- mudanca de taxonomia de tags;
- mudanca na hierarquia de decks.

Resposta esperada:
- tratar como mudanca controlada;
- exigir ADR quando impacto for estrutural;
- planejar migracao antes de alteracao ampla.

### 2. Aplicar politica de resposta

1. Falha nunca deve ser silenciosa.
2. Excecao deve gerar estado identificavel.
3. Toda recuperacao precisa preservar rastreabilidade.
4. Mudanca estrutural relevante deve ser registrada em ADR.

### 3. Registrar evidencia minima por erro

- data/hora;
- tipo de excecao;
- artefato afetado;
- causa provavel;
- acao recomendada.

## Validacao

- classes de excecao mapeadas por tipo de falha;
- resposta esperada definida para cada classe;
- politica de resposta com regra de nao-silenciamento;
- evidencia minima padronizada para auditoria.

## Troubleshooting

### Problema: falhas sem contexto para reprocessar

Acao recomendada:

- garantir registro completo da evidencia minima antes de encerrar o fluxo.

### Problema: conflitos sendo sobrescritos

Acao recomendada:

- bloquear merge silencioso e forcar estado conflict com trilha de decisao.

### Problema: mudancas estruturais sem governanca

Acao recomendada:

- abrir ADR antes de alterar taxonomia de tags, campos ou hierarquia de decks.

## Rastreabilidade

- Etapa/Subetapa: E4.S3
- Backlog: BLG-0016
- Dependencias: E4.S1, E4.S2, E3

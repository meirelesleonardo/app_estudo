# E4.S3 - Tratamento de Excecoes e Divergencias

## Objetivo

Definir como a futura integracao deve reagir a falhas, inconsistencias e conflitos sem perder rastreabilidade.

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

## Politica de resposta

1. Falha nunca deve ser silenciosa.
2. Excecao deve gerar estado identificavel.
3. Toda recuperacao precisa preservar rastreabilidade.
4. Mudanca estrutural relevante deve ser registrada em ADR.

## Evidencia minima por erro futuro

- data/hora;
- tipo de excecao;
- artefato afetado;
- causa provavel;
- acao recomendada.

## Rastreabilidade

- Etapa/Subetapa: E4.S3
- Backlog: BLG-0016
- Dependencias: E4.S1, E4.S2, E3

# Modelo de Rastreabilidade

## Objetivo

Garantir que toda decisao, requisito e item de backlog possam ser rastreados de ponta a ponta.

## Entidades

- Etapa (E#)
- Subetapa (E#.S#)
- Backlog (BLG-####)
- Decisao (ADR-####)
- SPEC (SPEC-...)
- Marco (M#)

## Regras

1. Todo item de backlog deve apontar para uma etapa.
2. Toda SPEC deve apontar para subetapa e backlog.
3. Toda ADR deve apontar para impactos em backlog e roadmap.
4. Mudancas de escopo devem atualizar roadmap e backlog no mesmo ciclo.

## Matriz de ligacao minima

- Etapa -> Subetapas
- Subetapa -> Backlog
- Backlog -> SPEC
- SPEC -> ADR (quando houver decisao relevante)
- Backlog -> Changelog (quando concluido)

## Criterios de qualidade da rastreabilidade

- completude: links obrigatorios preenchidos;
- consistencia: IDs validos e sem duplicidade;
- atualidade: status alinhado entre roadmap e backlog;
- auditabilidade: historico de decisao registrado.

## Exemplo de fluxo

1. Definir E2.S1 (curadoria de fontes).
2. Criar BLG-0012 para matriz de avaliacao.
3. Refinar e aprovar SPEC-E2-S1-001.
4. Registrar ADR caso haja decisao de criterio.
5. Atualizar changelog no fechamento.

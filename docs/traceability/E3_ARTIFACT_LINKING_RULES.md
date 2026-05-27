# E3.S2 - Regras de Vinculo entre Artefatos

## Objetivo

Definir como roadmap, backlog, SPEC, ADR, changelog, diario e marcos se vinculam de forma consistente.

## Principio central

Todo artefato relevante deve apontar para seu contexto de origem e para o impacto que produz.

## Regras por artefato

### Roadmap

Deve referenciar:
- etapas e status oficiais;
- marcos de conclusao;
- dependencias entre etapas.

### Phase Breakdown

Deve referenciar:
- decomposicao de cada etapa em subetapas;
- nomes curtos e estaveis para navegacao.

### Backlog

Deve referenciar:
- etapa ou subetapa de origem;
- criterio de conclusao;
- status atual.

Pode referenciar:
- SPECs relacionadas;
- ADRs afetadas.

### SPEC

Deve referenciar:
- etapa;
- subetapa;
- backlog relacionada;
- ADR relacionada, quando houver;
- changelog, quando concluida.

### ADR

Deve referenciar:
- problema que motivou a decisao;
- artefatos impactados;
- backlog e SPEC afetadas, quando houver.

### Changelog

Deve referenciar indiretamente:
- marcos fechados;
- backlog concluido;
- mudancas relevantes de status.

### Diario do projeto

Deve referenciar:
- etapa/subetapa trabalhada;
- backlog impactado;
- decisoes e riscos da sessao.

## Matriz de vinculo obrigatorio

| Artefato | Deve apontar para | Pode apontar para |
|---|---|---|
| Etapa | roadmap | backlog, marco |
| Subetapa | etapa | backlog, SPEC |
| Backlog | etapa/subetapa | SPEC, ADR, changelog |
| SPEC | backlog, etapa, subetapa | ADR, changelog |
| ADR | backlog ou SPEC impactada | roadmap, diario |
| Marco | roadmap, changelog | backlog, ADR |
| Diario | etapa/subetapa, backlog | ADR, marco |

## Regras de consistencia

1. Se o backlog mudar de status para Done, roadmap e changelog devem ser avaliados no mesmo ciclo.
2. Se uma SPEC for criada, o backlog correspondente nao pode permanecer sem referencia.
3. Se uma ADR alterar escopo, roadmap e backlog precisam refletir a decisao.
4. Se uma etapa for dada como concluida, todas as subetapas obrigatorias devem estar fechadas.

## Rastreabilidade

- Etapa/Subetapa: E3.S2
- Dependencias: E3.S1

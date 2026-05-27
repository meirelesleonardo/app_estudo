# E4.S2 - Fluxos Logicos de Sincronizacao

## Objetivo

Definir os fluxos documentais que orientarao a futura sincronizacao entre os artefatos curados do projeto e o Anki.

## Pre-requisitos

- modelo logico definido em E4.S1;
- rastreabilidade de artefatos validada em E3;
- politica de excecoes definida em E4.S3.

## Passos

### Fluxos principais

### 1. Criacao de nota nova

1. Item curado e validado entra no backlog implementavel.
2. Conteudo e normalizado para estrutura de nota.
3. Identificador unico e calculado.
4. Sistema verifica existencia previa no Anki.
5. Se nao existir, cria nota e vincula tags/deck/midia.
6. Registro de sincronizacao e atualizado.

### 2. Atualizacao de nota existente

1. Fonte original sofre alteracao ou refinamento.
2. Item e comparado com versao sincronizada.
3. Divergencias sao classificadas por impacto.
4. Nota existente e atualizada sem perder consistencia historica.

### 3. Reconciliacao de duplicidade

1. IDs ou metadados apontam colisao.
2. Sistema compara origem, trecho, tags e nivel.
3. Item e marcado para reconciliacao.
4. Politica de merge ou bloqueio e aplicada.

### 4. Sincronizacao de midia

1. Midia e localizada e validada.
2. Nota destino e confirmada.
3. Vinculo logico entre nota e midia e registrado.
4. Falhas de anexo geram estado pendente, nao descarte silencioso.

### Estados logicos de sincronizacao

- pending
- synced
- updated
- conflict
- blocked

### Regras de consistencia

1. Nenhuma nota deve ser criada sem identificador unico.
2. Nenhuma atualizacao deve sobrescrever origem sem trilha de mudanca.
3. Nenhuma midia deve ser vinculada sem referencia validada.
4. Conflitos devem gerar estado explicito e reprocessavel.

## Validacao

- fluxo de criacao, atualizacao, reconciliacao e midia documentados;
- estados logicos de sincronizacao definidos;
- regras de consistencia alinhadas com tratamento de excecoes;
- dependencias de E3 e E4.S1 explicitadas.

## Troubleshooting

### Problema: nota criada em duplicidade

Acao recomendada:

- revisar calculo de identificador unico;
- reforcar etapa de verificacao de existencia previa.

### Problema: conflito sem tratamento

Acao recomendada:

- garantir transicao para estado conflict e fila de reprocessamento.

### Problema: midia nao vinculada

Acao recomendada:

- validar referencia de midia antes da vinculacao e manter estado pending quando falhar.

## Metricas futuras

- taxa de criacao bem sucedida;
- taxa de atualizacao sem conflito;
- taxa de duplicidade evitada;
- tempo medio de reconciliacao.

## Rastreabilidade

- Etapa/Subetapa: E4.S2
- Backlog: BLG-0015
- Dependencias: E4.S1, E3

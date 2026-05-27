# Validacao de Legendas e Transcricoes (E2.S3)

## Contexto

A qualidade de legenda/transcricao define a confiabilidade do ciclo ouvir-entender-conferir.

## Objetivo

Padronizar como validar legendas e transcricoes para garantir uso seguro nas trilhas de listening.

## Escopo

- criterios objetivos de qualidade textual;
- fluxo de validacao por amostragem;
- classificacao de aprovacao do material;
- regra de revalidacao periodica.

## Fora do escopo

- geracao automatica de transcricao;
- correcao automatica por IA;
- automacao tecnica de pipeline.

## Criterios de validacao

1. Precisao lexical
- palavras-chave do trecho estao corretas;
- nomes proprios e termos tecnicos sem distorcao grave.

2. Sincronismo temporal
- legenda acompanha audio sem atraso relevante;
- blocos nao quebram sentido sem necessidade.

3. Integridade semantica
- sentido global do trecho preservado;
- contracoes e reducoes nao viram falso significado.

4. Cobertura
- ausencia de lacunas extensas sem transcricao;
- trechos de baixa audibilidade sinalizados.

5. Consistencia de estilo
- padrao de pontuacao minimamente uniforme;
- variacoes de fala natural representadas sem excesso de normalizacao.

## Fluxo de validacao

1. Selecionar amostra por nivel (A1-C1) e tipo de fonte.
2. Comparar audio e texto em trechos curtos.
3. Registrar nao conformidades por criterio.
4. Calcular score de confiabilidade.
5. Classificar material: Aprovado, Revisar, Reprovado.
6. Publicar observacoes no catalogo de fontes.

## Rubrica de confiabilidade (0-5)

| Criterio | Peso |
|---|---:|
| Precisao lexical | 30 |
| Sincronismo temporal | 20 |
| Integridade semantica | 25 |
| Cobertura | 15 |
| Consistencia de estilo | 10 |

Score final = soma(criterio x peso).

## Limiar de aprovacao

- >= 4.0: Aprovado;
- 3.0 a 3.9: Revisar;
- < 3.0: Reprovado para trilhas iniciais.

## Revalidacao

- fontes em uso: revalidacao trimestral;
- fontes em Revisar: revalidacao em ate 30 dias;
- mudanca de legenda oficial exige nova validacao.

## Entregaveis de E2.S3

- processo de validacao documentado;
- rubrica com pesos definida;
- limiares de aprovacao publicados.

## Rastreabilidade

- Etapa/Subetapa: E2.S3
- Backlog: BLG-0009
- Dependencias: BLG-0007, BLG-0008

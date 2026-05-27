# Pipeline de Conhecimento Confiavel

## Fluxo arquitetural oficial

```txt
Trusted Source
-> Curated Source
-> Validated Content
-> Normalized Content
-> Knowledge Unit
-> AI Processing
-> Study Asset
-> Anki Logical Note
-> Sync Pipeline
```

## Gates de qualidade por transicao

1. Trusted Source -> Curated Source
- classificacao de fonte valida;
- confiabilidade definida;
- mantenedor atribuido.

2. Curated Source -> Validated Content
- evidencias de revisao;
- ausencia de bloqueio normativo;
- data de expiracao valida.

3. Validated Content -> Normalized Content
- regra de normalizacao versionada;
- hash de entrada e saida;
- flags de transformacao registradas.

4. Normalized Content -> Knowledge Unit
- unidade semantica delimitada;
- vinculo a topico/disciplina;
- risco e confianca declarados.

5. Knowledge Unit -> AI Processing
- politica de uso por IA autorizando o tipo de automacao;
- trilha de lineage completa.

6. AI Processing -> Study Asset
- estrategia pedagogica declarada;
- metrica minima de qualidade definida.

7. Study Asset -> Anki Logical Note
- contrato de mapeamento validado;
- campos obrigatorios presentes.

8. Anki Logical Note -> Sync Pipeline
- status apto para sincronizacao;
- auditoria de ultimo estado registrada.

## Separacao obrigatoria bruto x curado

- RawTranscript: bruto, sem intervencao pedagogica;
- CuratedTranscript: curado e aprovado;
- NormalizedSentence: transformacao textual versionada;
- StudySegment: recorte didatico rastreavel;
- CuratedStudyItem: item apto para pipeline de estudo.

## Rastreabilidade

- Etapa/Subetapa: E2.S5
- Backlog: BLG-0037

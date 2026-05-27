# E6.S5 - Taxonomia e Ontologia de Cyber Seguranca

## Contexto

S5 formaliza a base semantica de conhecimento para organizar trilhas,
prerequisitos e clusters de estudo, com foco em RAG pedagogico rastreavel.

## Objetivo

Formalizar:
- dominios;
- subdominios;
- dependencias;
- prerequisitos;
- trilhas;
- clusters de conhecimento;
- relacoes semanticas.

## Mapa inicial de dominios

```txt
CyberSecurity
├── Redes
├── Linux
├── Criptografia
├── IAM
├── WebSecurity
├── Cloud
├── Malware
├── SIEM
├── ThreatIntel
├── SOC
├── LGPD
└── ISO27001
```

## Relacoes semanticas obrigatorias

- depends_on;
- prerequisite_for;
- equivalent_to;
- complements;
- applied_in.

## Regras de modelagem

- todo no semantico deve ter node_id unico;
- todo subdominio deve apontar dominio pai;
- toda trilha deve declarar prerequisitos minimos;
- todo cluster deve declarar fonte trusted associada.

## Riscos

- sobreposicao de conceitos sem normalizacao de vocabulos;
- lacunas de prerequisitos em trilhas aceleradas;
- ontologia crescer sem controle de versao.

## Dependencias

- E2.S5 para governanca de fontes;
- E6.S1 para curadoria por disciplina;
- E6.S4 para contrato de questoes por no semantico.

## Evolucao futura

- grafo semantico versionado para recomendacao adaptativa;
- alinhamento com QuestionBlueprint e AdaptiveReviewProfile;
- validacao automatizada de cobertura de topicos por banca.

## Rastreabilidade

- Etapa/Subetapa: E6.S5
- Backlog: BLG-0042, BLG-0043

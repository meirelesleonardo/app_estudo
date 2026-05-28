# Base Inicial - Provas de Concurso Cybersec para Cards

## Objetivo

Consolidar uma base rastreavel de questoes de concurso com:
- prova correta vinculada ao gabarito correspondente;
- resposta certa com evidencia;
- classificacao por assunto e subassunto;
- explicacao pedagogica com fontes confiaveis;
- preparo para criacao futura de cards no Anki.

## Escopo deste artefato

- processar 3 PDFs (2 provas + 1 gabarito, ou formato equivalente);
- extrair questoes, alternativas e resposta correta;
- gerar registro por questao com trilha de confianca;
- preparar base para etapa seguinte de criacao/sync de cards.

## Fora de escopo

- nao executa scraping;
- nao executa pipeline automatizado;
- nao envia cards automaticamente nesta etapa.

## Inventario de entrada (preencher)

| doc_id | nome_arquivo | tipo | observacao |
|---|---|---|---|
| PDF-01 | data/sources/concursos/raw/prova_cibersegurança.pdf | prova | Prova objetiva, Prova 2 - Analista / Analise de Sistemas - Ciberseguranca (manha) |
| PDF-02 | data/sources/concursos/raw/prova_cibersegurança2.pdf | prova | Prova discursiva, Prova 15 - Analista / Analise de Sistemas - Ciberseguranca (tarde) |
| PDF-03 | data/sources/concursos/raw/Gabarito_Final.pdf | gabarito | Gabarito final apos recursos, com coluna especifica para Prova 2 |

## Matriz de correspondencia prova x gabarito (preencher)

| prova_id | gabarito_id | criterio_de_vinculo | nivel_confianca |
|---|---|---|---|
| BNDES-2024-PROVA-2-OBJETIVA | BNDES-2024-GABARITO-FINAL | cabecalho edital 01/2024 + data 13/10/2024 + coluna Prova 2 no bloco de conhecimentos especificos | alta |
| BNDES-2024-PROVA-15-DISCURSIVA | N/A (sem gabarito objetivo associado) | prova discursiva sem chave objetiva A-E no gabarito final | alta |

Regra critica:
- nunca aplicar um gabarito sem confirmar codigo/versao correspondente da prova.

## Estrutura de registro por questao

Cada questao deve gerar um registro com os campos abaixo:

- exam_question_id (ex.: CBR-2026-PROVA-A-Q001)
- prova_id
- numero_questao
- pagina_prova
- enunciado
- alternativas (A-E)
- resposta_correta
- evidencia_gabarito (pagina/linha)
- assunto
- subassunto
- habilidade_cobrada
- nivel_dificuldade (basico/intermediario/avancado)
- explicacao_direta
- explicacao_aprofundada
- referencias_confiaveis
- status_curadoria
- revisado_por
- revisado_em

## Taxonomia sugerida de assunto (inicial)

- Redes
- Linux
- Criptografia
- IAM
- WebSecurity
- Cloud
- Malware
- SIEM
- ThreatIntel
- SOC
- LGPD
- ISO27001

## Politica de fontes para explicacao (obrigatoria)

Prioridade de referencia:
1. OWASP
2. NIST
3. CIS Benchmarks
4. MITRE ATT&CK
5. CISA
6. RFC Editor
7. Linux Foundation
8. Documentacao oficial de protocolos
9. Documentacao oficial de cloud providers

Regras:
- toda explicacao deve citar ao menos 1 fonte oficial/normativa;
- se usar fonte comunitaria, marcar como apoio e manter revisao humana;
- nao usar fonte experimental para resposta final sem validacao.

## Template de curadoria por questao

### Questao: PENDENTE
- Prova: PENDENTE
- Numero: PENDENTE
- Resposta correta: PENDENTE
- Evidencia de gabarito: PENDENTE
- Assunto: PENDENTE
- Subassunto: PENDENTE
- Habilidade cobrada: PENDENTE
- Explicacao direta: PENDENTE
- Explicacao aprofundada: PENDENTE
- Referencias confiaveis: PENDENTE
- Status de curadoria: draft

## Politica de qualidade

Uma questao so fica pronta para card quando:
- prova-gabarito estiver validado;
- resposta correta tiver evidencia;
- assunto/subassunto estiverem classificados;
- explicacao direta e aprofundada estiverem revisadas;
- referencias confiaveis estiverem registradas.

## Preparo para etapa de cards

Saida esperada desta fase:
- base curada por questao pronta para mapear em nota;
- identificador unico por questao;
- campo de resposta correta e explicacao auditaveis;
- tags por assunto/subassunto para filtros futuros.

## Rastreabilidade

- Etapa/Subetapa: E2.S5, E6.S4, E6.S5
- Backlog: BLG-0040, BLG-0041, BLG-0042, BLG-0043

# Guia de Estudo - BNDES 2024 Prova 2 (Ciberseguranca)

## Mapeamento de arquivos e confianca
- Prova objetiva: data/sources/concursos/raw/prova_cibersegurança.pdf (Prova 2 - Manha).
- Arquivo adicional identificado: prova_cibersegurança2.pdf (Prova discursiva, sem gabarito objetivo).
- Gabarito aplicado: data/sources/concursos/raw/Gabarito_Final.pdf (coluna Prova 2 para Q36-70 e bloco comum Q1-35).
- Confianca de correspondencia prova-gabarito: alta (cabecalho edital/data e identificacao de Prova 2).

## Resultado da extracao
- Questoes objetivas com resposta correta mapeada: 70/70.
- Enunciados e alternativas extraidos por OCR/text mining: base preliminar para revisao humana.
- Base estruturada: data/sources/concursos/processed/bndes_2024_prova2_objetiva_q1_q70_enriched.json
- Seed para cards: data/sources/concursos/processed/bndes_2024_prova2_cards_seed.csv

## Estrutura por bloco
- Q1-Q20: Conhecimentos Transversais (economia, sustentabilidade, políticas públicas).
- Q21-Q30: Lingua Portuguesa.
- Q31-Q35: Lingua Inglesa (reading comprehension).
- Q36-Q70: Conhecimentos Especificos de Ciberseguranca.

## Trilhas de estudo recomendadas (Ciberseguranca)
### Segurança de Endpoint e Malware
- Questoes relacionadas: 36.
- Fontes confiaveis para estudar: CIS Controls v8; NIST SP 800-83; Microsoft Security Baselines.
- Foco: deteccao/prevenção de malware, superficies de ataque em endpoints e politicas de execucao.

### SOC, SIEM e Resposta a Incidentes
- Questoes relacionadas: 37, 65.
- Fontes confiaveis para estudar: NIST SP 800-61r2; MITRE ATT&CK; CISA Incident Response Guides.
- Foco: triagem, correlacao, automacao (SOAR), playbooks e melhoria de MTTD/MTTR.

### Criptografia e Hash
- Questoes relacionadas: 38, 51, 55, 58, 60.
- Fontes confiaveis para estudar: NIST SP 800-57; NIST SP 800-52r2 (TLS); RFC 8446 (TLS 1.3).
- Foco: cifragem simetrica/assimetrica, integridade por hash, handshake TLS 1.2 vs 1.3, forward secrecy.

### Cibersegurança - geral
- Questoes relacionadas: 39, 48, 53, 66, 68.
- Fontes confiaveis para estudar: NIST CSF 2.0.

### IAM e Controle de Acesso
- Questoes relacionadas: 40, 42, 45, 46, 49, 50, 52, 54, 57, 59, 61, 63, 64, 69, 70.
- Fontes confiaveis para estudar: NIST SP 800-63; CIS Controls v8; OWASP ASVS (Authentication).
- Foco: fatores de autenticacao, federacao, protocolos (SAML/OAuth2/RADIUS), principio do menor privilegio.

### Governança, Risco e Compliance
- Questoes relacionadas: 41, 43, 44, 56, 62.
- Fontes confiaveis para estudar: ISO/IEC 27001/27002; NIST CSF 2.0; LGPD e guias ANPD.
- Foco: politicas, evidencia de controle, risco residual, alinhamento com normas e auditoria.

### Redes e Defesa Perimetral
- Questoes relacionadas: 47.
- Fontes confiaveis para estudar: NIST SP 800-41; RFCs de protocolos de rede; CISA Zero Trust Maturity Model.
- Foco: controles de borda, filtragem de trafego, segmentacao, defesa em profundidade.

### Segurança de Aplicações Web
- Questoes relacionadas: 67.
- Fontes confiaveis para estudar: OWASP Top 10; OWASP ASVS; MITRE CWE.
- Foco: classes OWASP Top 10, mitigacoes por design seguro e validacao de entrada/saida.

## Observacoes para criacao de cards
- O CSV seed ja traz frente, resposta correta, tema e referencias.
- Falta revisar qualidade de mapeamento enunciado/alternativas em parte das questoes antes de enviar ao Anki.
- Falta enriquecer o verso com explicacao individual por questao (passo seguinte recomendado).
- A prova discursiva foi identificada, mas nao entra no fluxo de gabarito objetivo.
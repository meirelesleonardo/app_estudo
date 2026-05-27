# Guia de Usabilidade do App

## Objetivo

Definir um fluxo simples e repetivel para usar o projeto no dia a dia, com foco em produtividade, qualidade dos cards e seguranca operacional.

## Publico-alvo

- mantenedor do projeto;
- contribuidores tecnicos;
- usuario que deseja estudar listening com suporte de automacao.

## Escopo deste guia

- preparar ambiente local;
- validar conectividade com AnkiConnect;
- executar fluxo minimo de sincronizacao;
- manter qualidade dos decks e das tags;
- registrar evidencias de execucao.

## Jornada recomendada de uso

1. Abrir Anki Desktop.
2. Confirmar que o add-on AnkiConnect esta ativo.
3. Ativar ambiente virtual do projeto.
4. Executar healthcheck do endpoint local.
5. Rodar scripts de sincronizacao/padronizacao quando necessario.
6. Validar resultado no Anki (deck, tags, campos e midia).
7. Registrar alteracoes relevantes no changelog e no journal.

## Fluxo operacional minimo

### 1. Preparar sessao

Linux:

```bash
cd /home/suporte/Projetos/app_estudo
source .venv/bin/activate
```

Windows PowerShell:

```powershell
cd C:\caminho\app_estudo
.venv\Scripts\activate
```

### 2. Testar endpoint do AnkiConnect

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/check_ankiconnect.py
```

Resultado esperado: status de conexao valido e versao retornada.

### 3. Executar padronizacao de deck (quando necessario)

Auditoria (sem mudanca):

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/standardize_anki_deck.py
```

Aplicacao efetiva:

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/standardize_anki_deck.py --apply
```

### 4. Executar saneamento qualitativo

Auditoria:

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/sanitize_anki_quality.py
```

Aplicacao:

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/sanitize_anki_quality.py --apply
```

## Padrao de qualidade para uso diario

- manter deck padrao no formato Ingles::Listening::<nivel>;
- evitar tags soltas fora da convencao do projeto;
- revisar cards novos no Anki apos cada execucao de script;
- executar primeiro em modo auditoria e aplicar depois;
- evitar rodar scripts de alteracao com Anki fechado.

## Checklist rapido de usabilidade

- [ ] Anki aberto e funcional.
- [ ] AnkiConnect respondendo em http://localhost:8765.
- [ ] Ambiente virtual ativo.
- [ ] Scripts executados sem erro.
- [ ] Deck e tags validados no Anki.
- [ ] Evidencia registrada em docs/journal/PROJECT_JOURNAL.md (se aplicavel).

## Problemas frequentes

### AnkiConnect indisponivel

Possiveis causas:

- Anki nao esta aberto;
- add-on nao instalado;
- bloqueio por firewall;
- porta 8765 em conflito.

Acao recomendada:

1. Reabrir Anki.
2. Confirmar instalacao do add-on 2055492159.
3. Testar endpoint no navegador.
4. Reexecutar script de healthcheck.

### Mudancas nao aparecem no deck

Possiveis causas:

- execucao em modo auditoria sem --apply;
- filtro de migracao muito restritivo;
- deck de origem diferente do esperado.

Acao recomendada:

1. Revisar parametros do comando.
2. Rodar auditoria e conferir o resumo retornado.
3. Aplicar novamente com escopo correto.

## Boas praticas de seguranca operacional

- manter backup/sync do AnkiWeb ativo;
- nao aplicar migracoes em lote sem auditoria previa;
- evitar uso de flags forcadas sem necessidade;
- tratar cada execucao como operacao rastreavel (o que rodou, quando e com qual resultado).

## Referencias relacionadas

- docs/integrations/ANKI_ENV_SETUP.md
- docs/integrations/E4_LOGICAL_MODEL.md
- docs/integrations/E4_SYNC_FLOWS.md
- docs/integrations/E4_EXCEPTION_HANDLING.md
- docs/journal/PROJECT_JOURNAL.md

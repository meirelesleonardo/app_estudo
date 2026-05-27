# Instalacao do Ambiente - Linux Mint e Windows 11

Este guia prepara o ambiente para desenvolvimento e integracao com o Anki via AnkiConnect.

## Objetivo

Garantir:

- ambiente funcional;
- integracao com API do Anki;
- preparacao para automacoes futuras;
- compatibilidade com o projeto.

## Pre-requisitos

- acesso administrativo para instalacao local (quando necessario);
- acesso a internet para downloads oficiais;
- Anki Desktop e Python suportados no sistema operacional.

## Arquitetura esperada

```txt
VS Code
↓
Python
↓
AnkiConnect
↓
Anki Desktop
↓
AnkiWeb Sync
↓
AnkiDroid / Mobile
```

## Requisitos gerais

| Ferramenta | Finalidade |
| --- | --- |
| Python | automacoes |
| VS Code | desenvolvimento |
| Anki Desktop | revisao espacada |
| AnkiConnect | API HTTP local |
| Git | versionamento |
| venv | isolamento Python |

## Passos

## Instalacao - Linux Mint

### 1. Atualizar sistema

```bash
sudo apt update
```

### 2. Instalar dependencias

```bash
sudo apt install curl wget zstd libxcb-xinerama0 libxcb-cursor0 libnss3 git python3 python3-pip python3-venv
```

### 3. Baixar o Anki

Acessar: https://apps.ankiweb.net/

Selecionar a versao:

```txt
Linux Qt6
```

Arquivo esperado:

```txt
anki-25.xx-linux-qt6.tar.zst
```

### 4. Extrair pacote

```bash
cd ~/Downloads
tar xaf anki-*-linux-qt6.tar.zst
```

### 5. Entrar na pasta

```bash
cd anki-*-linux-qt6
```

### 6. Instalar Anki

```bash
sudo ./install.sh
```

### 7. Executar Anki

```bash
anki
```

Ou via menu do Linux Mint, pesquisando por Anki.

## Instalacao - Windows 11

### 1. Instalar Python

Download: https://www.python.org/downloads/windows/

Durante a instalacao, marcar:

```txt
Add Python to PATH
```

Validar:

```powershell
python --version
```

### 2. Instalar Git

Download: https://git-scm.com/download/win

Validar:

```powershell
git --version
```

### 3. Instalar VS Code

Download: https://code.visualstudio.com/download

Durante a instalacao, habilitar:

- Add to PATH
- Open with Code

### 4. Instalar Anki

Download: https://apps.ankiweb.net/

Selecionar a versao:

```txt
Windows Qt6
```

Concluir instalacao padrao e abrir o app.

## Configuracao inicial do Anki

### 1. Criar conta AnkiWeb

No Anki:

```txt
Sync
-> Create Account
```

Essa conta sera usada para sincronizacao, backup e uso em dispositivos moveis.

## Instalar AnkiConnect

### 1. Abrir menu de add-ons

No Anki:

```txt
Tools
-> Add-ons
-> Get Add-ons
```

### 2. Inserir codigo

```txt
2055492159
```

Repositorio oficial: https://github.com/amikey/anki-connect

### 3. Reiniciar o Anki

Fechar e abrir novamente para carregar o add-on.

## Validacao

### Validar API do AnkiConnect

Endpoint padrao:

```txt
http://localhost:8765
```

### Teste via navegador

Abrir http://localhost:8765 e confirmar resposta do servico.

### Teste via curl - Linux

```bash
curl localhost:8765
```

### Teste via PowerShell - Windows

```powershell
curl http://localhost:8765
```

### Teste real da API

Linux:

```bash
curl localhost:8765 -X POST -d '{"action":"version","version":6}'
```

Windows PowerShell:

```powershell
curl http://localhost:8765 -Method POST -Body '{"action":"version","version":6}'
```

Resposta esperada:

```json
{"result":5,"error":null}
```

## Operacao no Projeto

### Healthcheck local

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/check_ankiconnect.py
```

### Padronizacao de deck legado

Auditar sem alterar:

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/standardize_anki_deck.py
```

Aplicar padronizacao segura (somente candidatos com assinatura do projeto):

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/standardize_anki_deck.py --apply
```

### Saneamento qualitativo

Auditar sem alterar:

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/sanitize_anki_quality.py
```

Aplicar saneamento:

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/sanitize_anki_quality.py --apply
```

### Reconciliacao de duplicatas (CSP-004)

Dry-run (nao altera):

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/reconcile_anki_duplicates.py --deck Ingles::Listening::B1
```

Aplicar reconciliacao:

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/reconcile_anki_duplicates.py --deck Ingles::Listening::B1 --apply
```

## Estrutura inicial do projeto

### Criar pasta do projeto

Linux:

```bash
mkdir study-automation
cd study-automation
```

Windows PowerShell:

```powershell
mkdir study-automation
cd study-automation
```

### Criar ambiente virtual Python

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Instalar dependencia inicial

```bash
pip install requests
```

Estrutura recomendada:

```txt
study-automation/
|- app_estudo/
|- docs/
|- scripts/
|- tests/
|- prompts/
|- .venv/
|- README.md
|- requirements.txt
|- .gitignore
```

## Integracao com scripts do repositorio

Com Anki aberto, validar via script interno:

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/check_ankiconnect.py
```

## Operacao de padronizacao e saneamento (opcional)

- Auditar migracao de deck: /home/suporte/Projetos/app_estudo/.venv/bin/python scripts/standardize_anki_deck.py
- Aplicar migracao segura: /home/suporte/Projetos/app_estudo/.venv/bin/python scripts/standardize_anki_deck.py --apply
- Forcar migracao total (uso cauteloso): /home/suporte/Projetos/app_estudo/.venv/bin/python scripts/standardize_anki_deck.py --apply --force-all-source
- Auditar qualidade das notas: /home/suporte/Projetos/app_estudo/.venv/bin/python scripts/sanitize_anki_quality.py
- Aplicar saneamento: /home/suporte/Projetos/app_estudo/.venv/bin/python scripts/sanitize_anki_quality.py --apply

## Extensoes recomendadas do VS Code

- Python: https://marketplace.visualstudio.com/items?itemName=ms-python.python
- Pylance: https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance
- Markdown All in One: https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one
- GitLens: https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens
- Error Lens: https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens

## Troubleshooting

### Problemas comuns

### Porta 8765 nao responde

Possiveis causas:

- Anki fechado;
- AnkiConnect nao instalado;
- firewall;
- conflito de porta.

### Python nao encontrado

Windows: reinstalar marcando Add Python to PATH.

Linux:

```bash
python3 --version
```

## Criterios de pronto do ambiente

- Anki inicia sem erro;
- AnkiConnect responde no endpoint local;
- script de healthcheck do repositorio finaliza com sucesso;
- ambiente Python ativo com venv no projeto.

## Rastreabilidade

- Etapa/Subetapa: E4.S1-E4.S3, E5.S2
- Backlog relacionado: BLG-0010, BLG-0015, BLG-0016, BLG-0017

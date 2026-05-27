# Quick Start - App Estudo

Guia resumido para deixar o ambiente funcional e executar o fluxo minimo em poucos minutos.

## Objetivo

Validar rapidamente que Anki, AnkiConnect e scripts do projeto estao operacionais.

## Pre-requisitos

- Anki Desktop instalado;
- add-on AnkiConnect instalado (codigo 2055492159);
- Python e venv disponiveis;
- repositorio clonado localmente.

## Passos

### 1. Abrir Anki

- iniciar o Anki Desktop;
- confirmar que o AnkiConnect carregou apos o restart.

### 2. Ativar ambiente do projeto

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

### 3. Validar API local

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/check_ankiconnect.py
```

Resultado esperado: conexao valida com endpoint http://localhost:8765.

### 4. Rodar auditoria de padronizacao

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/standardize_anki_deck.py
```

### 5. Rodar auditoria de saneamento

```bash
/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/sanitize_anki_quality.py
```

## Validacao

- Anki aberto sem erro;
- endpoint 8765 respondendo;
- healthcheck concluido;
- scripts de auditoria executados.

## Troubleshooting

### Porta 8765 nao responde

- confirmar que o Anki esta aberto;
- confirmar instalacao do add-on;
- testar http://localhost:8765 no navegador.

### Script falha por ambiente Python

- reativar .venv;
- confirmar dependencias instaladas;
- reexecutar comando.

## Proximo passo

Para guia completo, consultar:

- docs/integrations/ANKI_ENV_SETUP.md
- docs/usability/APP_USABILITY_GUIDE.md

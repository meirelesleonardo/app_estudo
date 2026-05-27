# Preparacao de Ambiente para AnkiConnect

## Objetivo

Padronizar a preparacao local minima para habilitar conexao com Anki no inicio da fase de integracao real.

## Quando preparar

- Preparar imediatamente apos concluir o mapeamento logico (CSP-003).
- Iniciar chamadas reais no incremento seguinte de integracao (proximo passo tecnico).

## Passos locais

1. Instalar o Anki Desktop (versao atual estavel).
2. Abrir o Anki e instalar o add-on AnkiConnect.
3. Reiniciar o Anki para carregar o add-on.
4. Confirmar que a porta padrao 8765 esta acessivel localmente.

## Verificacao minima

- Com Anki aberto, executar um ping para AnkiConnect:
- endpoint esperado: http://127.0.0.1:8765
- acao esperada: version

Comando sugerido no repositorio:

`/home/suporte/Projetos/app_estudo/.venv/bin/python scripts/check_ankiconnect.py`

## Criterios de pronto de ambiente

- Anki inicia sem erro.
- AnkiConnect responde no endpoint local.
- Deck de teste pode ser listado por chamada de consulta (quando habilitarmos o cliente).

## Validacao tecnica apos preparo

- Executar healthcheck local.
- Em seguida, usar o cliente de integracao para fluxo create/update com nota de teste.
- Modulo do cliente: app_estudo/integrations/ankiconnect_client.py

## Riscos operacionais

- firewall local bloqueando porta 8765;
- AnkiConnect desatualizado;
- execucao sem Anki aberto.

## Rastreabilidade

- Etapa/Subetapa: E4.S1-E4.S3, E5.S2
- Backlog relacionado: BLG-0010, BLG-0015, BLG-0016, BLG-0017

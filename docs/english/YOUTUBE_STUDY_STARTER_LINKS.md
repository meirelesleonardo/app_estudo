# Starter de Links YouTube para Listening

## Objetivo

Oferecer um conjunto inicial, curado e pratico de links para estudo de listening
com boa chance de legenda/transcript e progressao de dificuldade.

## Quando extrair o primeiro video

Voce ja pode extrair hoje, imediatamente, porque o pipeline de transcript e ingestao
esta implementado e testado. Com a dependencia `yt-dlp` instalada, tambem ja pode
extrair audio no mesmo fluxo.

## Primeiro video recomendado (B1)

- Fonte: TED
- Link: https://www.youtube.com/watch?v=eIho2S0ZahI
- Titulo: How to speak so that people want to listen | Julian Treasure
- Motivo: fala clara, estrutura organizada e boa utilidade para treino de escuta guiada.

## Lista curada por nivel

### A1-A2 (entrada e clareza)

1. BBC Learning English (canal): https://www.youtube.com/@bbclearningenglish
2. VOA Learning English (canal): https://www.youtube.com/@VOALearningEnglish
3. Speak English With Mr Duncan (canal): https://www.youtube.com/@duncaninchina

### B1-B2 (ritmo natural controlado)

1. TED (canal): https://www.youtube.com/@TED
2. BBC 6 Minute English (playlist/canal): https://www.youtube.com/results?search_query=bbc+6+minute+english
3. English Addict with Mr Duncan (conversas): https://www.youtube.com/@duncaninchina

### B2-C1 (densidade e espontaneidade)

1. Big Think (canal): https://www.youtube.com/@bigthink
2. Stanford Graduate School of Business (talks): https://www.youtube.com/@stanfordgsb
3. Talks at Google (canal): https://www.youtube.com/@TalksAtGoogle

## Configuracao minima recomendada

1. Confirmar dependencias Python:
   - `pip install -r requirements.txt`
2. Para extracao de audio com maior compatibilidade, manter ffmpeg instalado no sistema.
3. Executar smoke test com transcript e audio:
   - `PYTHONDONTWRITEBYTECODE=1 /home/suporte/Projetos/app_estudo/.venv/bin/python scripts/smoke_youtube_ingestion.py --url "https://www.youtube.com/watch?v=eIho2S0ZahI" --title "How to speak so that people want to listen" --db-path "data/audit/media_artifacts.db" --languages "en" --extract-audio --audio-output-dir "data/media/audio"`

## Checklist de qualidade do lote inicial

- transcript retornado sem vazio;
- quality_gate_status igual a approved;
- pelo menos 1 segmento gerado;
- arquivo de audio salvo em data/media/audio.

## Rastreabilidade

- Etapa/Subetapa: E2.S4
- SPEC relacionada: SPEC-E2-S4-007
- ADR relacionada: ADR-0001

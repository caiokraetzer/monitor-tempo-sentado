# Coleta de 03/11/2026 — Wokwi, HiveMQ e Node-RED

Consulte o [relato da execução](../../../docs/RESULTADOS_WOKWI.md) para método, resultados, problemas encontrados e limites.

| Arquivo | Conteúdo |
|---|---|
| `mqtt-receptor.jsonl` e `mqtt-receptor.csv` | 132 mensagens realmente recebidas pelo segundo assinante, em Python/paho. O JSONL mantém também o payload UTF-8 e as flags de recepção. |
| `node-red.jsonl` e `node-red.csv` | 132 mensagens recebidas e aceitas pelo fluxo Node-RED. |
| `metadados.json` | Metadados originais do coletor; seu commit identifica o receptor, não todas as revisões do firmware feitas durante o ensaio. |
| `verificacoes.json` | Sete verificações integradas aprovadas. |
| `node-red.log` | Inicialização, versões, conexão do broker e encerramento do fluxo. |
| `sessao-corrigida.jsonl` | Recorte derivado dos 82 registros da última sessão, delimitada pela redução do uptime após reinício. |
| `eventos.csv` | Dois inícios, quatro lembretes e um fim recebidos pelo Node-RED. |
| `analise.json` | Contagens, sessões, temporização, hashes das fontes e limites da análise. |
| `serial-observado.txt` | Trechos transcritos do monitor serial; não é uma captura serial completa. |

Os arquivos completos preservam duas sessões de diagnóstico e a sessão corrigida. Não descarte as tentativas anteriores ao interpretar as contagens. Os valores de carga foram simulados; as mensagens e os horários de recepção foram observados na execução.

[Execução e artefatos originais no GitHub Actions](https://github.com/caiokraetzer/monitor-tempo-sentado/actions/runs/41676404537).

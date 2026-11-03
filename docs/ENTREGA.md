# Repositório na entrega final

A exigência compartilhada do professor define o conjunto **artigo + vídeo-demonstração do funcionamento com MQTT + repositório contendo dados e código-fonte**. O artigo deve manter os requisitos das etapas anteriores. Este repositório atende à preparação do código e dos dados para reprodução; a comprovação integrada depende da execução e das evidências.

| Item | Onde está / ação necessária |
|---|---|
| Fonte ESP32 | `firmware/ChairMonitor/`. |
| Montagem simulada e bibliotecas | `diagram.json`, `libraries.txt`, `platformio.ini`, `wokwi.toml`. |
| MQTT e painel | `node-red/flows.json`, fontes do painel e `docs/MQTT.md`. |
| Instruções de reprodução | `README.md`, `docs/EXECUCAO.md` e `docs/MONTAGEM.md`. |
| Dados | Entradas e exemplo sintéticos identificados; coleta efetiva em [2026-11-03-wokwi-mqtt](../dados/coletas/2026-11-03-wokwi-mqtt/), com JSONL, CSV, metadados e análise. |
| Verificação do código | Testes e workflow; consultar o estado efetivo em `docs/VALIDACAO.md` e no GitHub Actions. |
| Simulação publicada | [Projeto Wokwi](https://wokwi.com/projects/479686134986460161) executado com recepção MQTT. Inserir o link também no artigo. |
| Vídeo com MQTT | Ainda não gravado; mostrar circuito, estados, buzzer, publicação e recebimento remoto. Inserir o link real no artigo e README. |
| Artigo final | Incorporar o ensaio exploratório de [RESULTADOS_WOKWI.md](RESULTADOS_WOKWI.md), distinguir simulação de montagem física e inserir os links reais. Revisão do Word em etapa separada. |

## Roteiro sugerido para a demonstração

Mostre brevemente os componentes e as conexões, o código e o prefixo MQTT. Inicie o Node-RED e o circuito com carga zero. Aplique 20 kg e mostre `inicio`, tempo e estado no receptor. Demonstre uma retirada breve sem encerrar, o primeiro lembrete e o buzzer, depois a retirada sustentada com `fim`. Mostre o CSV/JSONL efetivamente coletado. Se acelerar ou editar o vídeo, explique o recorte e preserve os registros originais.

Antes da submissão, abra os links de repositório, vídeo e simulação em sessão sem login ou confirme o acesso exigido pelo professor. A existência dos arquivos não garante acesso externo se o repositório estiver privado.

Os critérios do projeto final fornecidos pelo professor foram conferidos em 03/11/2026. O item 2.1 destina até 2,0 pontos à documentação do repositório; o vídeo vale até 3,0 pontos. A correspondência de cada requisito está em [CRITERIOS_AVALIACAO.md](CRITERIOS_AVALIACAO.md). A ausência de vídeo, repositório ou ambos resulta em nota zero segundo a rubrica, e o descumprimento de internet/MQTT limita a nota a um quarto do total. A comprovação da execução e a inserção dos links reais no artigo continuam necessárias.

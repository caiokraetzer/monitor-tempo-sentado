# Execução integrada Wokwi e recebimento MQTT — 03/11/2026

Foi executado o caminho **ESP32 simulado no Wokwi → broker HiveMQ na internet → Node-RED e um segundo assinante Python**. Os receptores registraram mensagens efetivamente recebidas do broker; não foram utilizados publicadores de dados fabricados.

- [Simulação salva](https://wokwi.com/projects/479686134986460161).
- [Execução do receptor e artefatos originais](https://github.com/caiokraetzer/monitor-tempo-sentado/actions/runs/41676404537).
- [Fonte exata da montagem corrigida](https://github.com/caiokraetzer/monitor-tempo-sentado/tree/9ba0d0cf415ce25dfacdc744615f53dcc574a4df).
- [Dados coletados](../dados/coletas/2026-11-03-wokwi-mqtt/).
- [Eventos em CSV](../dados/coletas/2026-11-03-wokwi-mqtt/eventos.csv).

## Ambiente e método

O Wokwi executou o firmware com perfil de lembrete de 60 s, sensor HX711 virtual de 50 kg, ESP32 DevKit V1 e buzzer. A carga foi alterada manualmente na interface, partindo de zero para tara. Foram aplicadas ocupação de 20 kg, redução a 9 kg, retirada breve, retorno a 20 kg, retirada sustentada e retorno.

O Node-RED executou no runner Linux do GitHub Actions com o fluxo do repositório. O log confirma Node-RED 4.1.17, Node.js 22.23.4 e FlowFuse Dashboard 1.34.1. Seu cliente assinou `mack/ods3/7c92a1/cadeira01/+` em `broker.hivemq.com:1883`; um cliente paho independente assinou o mesmo prefixo. Ambos utilizaram MQTT 3.1.1 e QoS 0. O endpoint `/dashboard/cadeira` respondeu HTTP 200.

A captura começou em 2026-11-03T16:39:41.488709+00:00 e terminou em 2026-11-03T16:51:30.122237+00:00. As datas dos receptores estão em UTC; a temporização do firmware utiliza `uptime_ms` da simulação.

## Resultados de recepção

| Verificação | Observado |
|---|---:|
| Mensagens recebidas pelo Node-RED | 132 |
| Mensagens recebidas pelo cliente paho | 132 |
| Telemetrias por receptor | 120 |
| Eventos por receptor | 7 |
| Mensagens de status por receptor | 5 |
| Divergências na comparação dos multiconjuntos de tópico e payload | 0 |
| Verificações integradas do coletor | 7 aprovadas |

Foram comparados tópico e conteúdo das mensagens, sem comparar o horário de recepção próprio de cada cliente. A correspondência entre os dois receptores não demonstra ausência de perdas comuns: MQTT QoS 0 continua sem garantia de entrega.

## Eventos recebidos da sessão corrigida

| Evento | Uptime simulado (ms) | Tempo do ciclo (s) | Recebido pelo Node-RED (UTC) |
|---|---:|---:|---|
| inicio | 41426 | 0.000 | 2026-11-03T16:45:40.894Z |
| lembrete | 101432 | 60.006 | 2026-11-03T16:46:43.560Z |
| lembrete | 161440 | 120.014 | 2026-11-03T16:47:48.340Z |
| lembrete | 221446 | 180.020 | 2026-11-03T16:48:56.332Z |
| lembrete | 281454 | 240.028 | 2026-11-03T16:49:59.976Z |
| fim | 309993 | 268.567 | 2026-11-03T16:50:30.851Z |
| inicio | 355013 | 0.000 | 2026-11-03T16:51:19.739Z |

O primeiro lembrete ocorreu **60,006 s após o início confirmado**, diferença de 6 ms em relação ao intervalo configurado de 60 s. As três repetições seguintes ficaram separadas por 60,008 s, 60,006 s e 60,008 s. A diferença de 6 ms do primeiro lembrete ficou dentro da meta inicial de 0,5 s para esse evento observado.

O ciclo encerrado durou 268,567 s, incluindo a janela de confirmação de saída. O evento seguinte iniciou um novo ciclo com tempo zero. Esses valores são do relógio simulado; não são latência de rede ou duração do tempo de parede.

A observação do serial também mostrou 8.400 unidades brutas para 20 kg e 3.780 para 9 kg, coerentes com o fator virtual de 420 unidades/kg. A ocupação foi preservada a 9 kg e durante a retirada breve. Trechos efetivamente observados estão em [serial-observado.txt](../dados/coletas/2026-11-03-wokwi-mqtt/serial-observado.txt). Os instantes de alteração manual da carga não foram medidos com precisão suficiente para calcular separadamente o atraso completo de entrada e saída.

## Problemas encontrados e correções

| Problema observado | Correção e evidência |
|---|---|
| O nome `HX711@0.7.5` não foi encontrado no catálogo do Wokwi. | Usado `HX711 Arduino Library@0.7.5`; o identificador do PlatformIO continua `bogde/HX711@0.7.5`. |
| O sensor não respondia à carga porque o diagrama usava `esp:19`, `esp:18` e `esp:23` no modelo DevKit V1. | Corrigidos para `esp:D19`, `esp:D18` e `esp:D23`. Depois disso, foram observadas leituras de 20 kg e 9 kg e os eventos do ciclo. Os GPIOs do firmware permanecem 19, 18 e 23. |
| A simulação avançava lentamente em segundo plano. | A aba foi mantida em primeiro plano; a espera do laço é de 10 ms, com aquisição aproximadamente a cada 100 ms. |
| Era necessário distinguir carga não lida de uma falha da lógica. | Incluído diagnóstico serial da amostra bruta, tara e carga filtrada, sem mudar o contrato MQTT. |

As duas primeiras sessões de diagnóstico foram preservadas nos arquivos completos: possuem 42 e 8 registros no Node-RED e não geraram eventos de ocupação. A sessão corrigida possui 82 registros e todos os sete eventos. O arquivo `sessao-corrigida.jsonl` é um recorte derivado; os arquivos `node-red.jsonl` e `mqtt-receptor.jsonl` conservam as três sessões.

## Proveniência das fontes e dos dados

O campo `fonte_commit` dos metadados originais é `e37aac1704d44b9cc20246aeddcee3beb962dbdd`: identifica o checkout do receptor. Durante a captura, a montagem e os diagnósticos do firmware foram corrigidos no editor do Wokwi. A fonte final foi baixada pelo comando “Download project ZIP”, comparada e publicada no commit `9ba0d0cf415ce25dfacdc744615f53dcc574a4df`.

| Arquivo final, normalizado para LF | SHA-256 |
|---|---|
| `sketch.ino` / `ChairMonitor.ino` | `0e6c144f95fca3281c8c0ef14809b69e6cf51dffe5324c6e7dd5eda43c12dfb2` |
| `diagram.json` | `52e5f116cea9c5128e62aaa8e6e1468cfbb3f606e605efa28bda7f3556fc67c0` |

As cópias textuais dos arquivos de captura foram extraídas dos blocos `BEGIN_CAPTURE_FILE` dos logs do job; as quebras de linha estão normalizadas para LF. O artefato ZIP original da execução é `coleta-wokwi-mqtt`, ID 13250672695, com digest informado pelo GitHub `sha256:01aebb84958c76d0e025379998ef83cda47bc6070638bbe8d695dd0684cf82ce`. O original inclui também o lockfile npm do receptor e fica disponível conforme o prazo de retenção do GitHub.

## Alcance da validação

Esta foi uma **demonstração integrada exploratória**, com um ciclo encerrado e início de outro. Não representa cinco repetições de todos os casos do plano. As falhas controladas de rede e sensor, a forma de onda e a duração dos pulsos do buzzer não foram medidas nesta coleta. A interface do painel respondeu e seu fluxo recebeu mensagens, mas a renderização visual do painel no runner não foi inspecionada.

Os estímulos do sensor são sintéticos, próprios da simulação. As mensagens e os horários de recepção são registros reais da transmissão desses estímulos. O ensaio não comprova montagem física, precisão mecânica, redução do comportamento sedentário ou eficácia clínica.

O vídeo no YouTube e a atualização do artigo com os links e resultados continuam como etapas da entrega acadêmica.

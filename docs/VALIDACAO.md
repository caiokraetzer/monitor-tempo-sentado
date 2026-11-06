# Estado da verificação — atualização de 05/11/2026

## Verificações aprovadas

| Verificação | Resultado / evidência |
|---|---|
| Processamento do painel | 5 testes automatizados aprovados. |
| Exportação JSONL para CSV | 2 testes automatizados aprovados. |
| JSON, conexões do fluxo e sincronização dos arquivos | Aprovados. |
| Lógica C++ nativa do firmware | 40 cenários aprovados: 8 casos x 5 repetições. |
| Compilação ESP32 | Aprovada nos perfis de 60 s e 1.800 s. |
| Node-RED, fluxo e endpoint do painel | Node-RED 4.1.17 iniciou, conectou ao broker e gravou mensagens; endpoint do painel respondeu HTTP 200. |
| Wokwi → HiveMQ → Node-RED e assinante Python | 132 mensagens por receptor, com os mesmos tópicos e conteúdos na comparação dos multiconjuntos. |
| Ciclo observado | Início, quatro lembretes, fim e novo início recebidos remotamente. |

- [Testes e compilação da fonte corrigida](https://github.com/caiokraetzer/monitor-tempo-sentado/actions/runs/41679535901).
- [Execução do receptor e coleta MQTT](https://github.com/caiokraetzer/monitor-tempo-sentado/actions/runs/41676404537).
- [Resultados, problemas corrigidos e limites](RESULTADOS_WOKWI.md).
- [Dados efetivamente coletados](../dados/coletas/2026-11-03-wokwi-mqtt/).

O commit da fonte simulada da coleta inicial é `9ba0d0cf415ce25dfacdc744615f53dcc574a4df`. Seus hashes e a diferença entre o checkout do receptor e a fonte corrigida estão registrados no relato. Os dados brutos preservam as tentativas de diagnóstico e a sessão corrigida.

## Limites

A coleta é um ensaio exploratório com um ciclo completo e novo início, sem cinco repetições de todos os casos. As falhas de rede e sensor não foram injetadas de maneira controlada na sessão corrigida. A forma de onda e a duração dos pulsos do buzzer não foram medidas. A renderização visual do painel no runner não foi inspecionada; foram verificados seu endpoint, a inicialização do fluxo e o registro das mensagens.

Não foram executados montagem mecânica física, ensaios com pessoas ou avaliação clínica. O artigo Word foi atualizado com os resultados, imagens, gráficos e links das duas campanhas. O vídeo no YouTube será gravado pelos autores antes da submissão.

## Verificações adicionais — 05/11/2026

- Versão instrumentada compilada e executada no Wokwi; ZIP e hashes publicados com a coleta.
- Quatro detecções de ocupação e quatro confirmações GPIO recebidas por MQTT.
- Cinco testes do painel e dois testes de exportação novamente aprovados.
- Quatro novos testes da análise temporal aprovados: correlação com deslocamento conhecido, necessidade de sondas, quatro observações e confirmação GPIO.
- Validador JSON/fluxo/sincronização novamente aprovado.
- As novas verificações não substituem os ensaios físicos nem o vídeo exigido.

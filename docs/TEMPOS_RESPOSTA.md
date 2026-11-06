# Tempos de resposta — ensaio de 5 de novembro de 2026

Foram realizadas quatro detecções confirmadas do HX711 e enviados quatro comandos reais de teste ao buzzer pelo broker HiveMQ. O vídeo acadêmico será gravado posteriormente.

## Fonte, coleta e reprodução

- [Simulação salva](https://wokwi.com/projects/479686134986460161).
- [Fonte exata baixada do Wokwi](../dados/coletas/2026-11-05-tempos-resposta/execucao-03-9fd31c/fonte-wokwi-executada.zip).
- [Dados da execução definitiva](../dados/coletas/2026-11-05-tempos-resposta/execucao-03-9fd31c/).
- [Tabela de medidas e margens](../dados/coletas/2026-11-05-tempos-resposta/execucao-03-9fd31c/tempos-resposta.csv).
- [Análise reproduzível](../scripts/analisar_tempos.py).

Instale requirements.txt e execute, na raiz do projeto:

~~~sh
python scripts/medir_tempos.py --output dados/coletas/nova-medicao --seconds 900
~~~

O diretório deve ser novo. O coletor assina mack/ods3/7c92a1/cadeira01/#, envia sondas de relógio a cada 1,5 s e, após oito respostas, envia quatro comandos teste_buzzer separados por pelo menos 4 s. A interface funciona em http://127.0.0.1:8765 durante a coleta.

Inicie o Wokwi com 0 kg para tara. Aguarde a mensagem ENSAIO 9fd31c: MQTT pronto e respostas às sondas. Aplique 20 kg até o evento inicio. Retire a carga e aguarde fim (mais de 10 s abaixo de 5 kg filtrados). Repita até obter quatro eventos instrumentados. Na última ocupação, mantenha a carga por mais de 60 s para demonstrar o lembrete automático. As alterações de carga são feitas no HX711 do Wokwi; o coletor não publica leituras de sensor.

O coletor grava coleta.json ao concluir. Para encerrá-lo antecipadamente, crie um arquivo vazio chamado parar dentro do diretório da execução. Depois execute:

~~~sh
python scripts/analisar_tempos.py dados/coletas/nova-medicao
~~~

## O que foi cronometrado

Sensor: a confirmação de ocupação após filtro e janela de 2 s é marcada por esp_timer_get_time(). A mensagem /sensor transporta identificador e detected_us; o assinante externo registra a recepção. A medida começa na detecção confirmada, não na alteração manual da carga.

Atuador: o emissor registra o envio de /comando com identificador. O ESP32 recebe a ordem e o laço local inicia o padrão sonoro. Um observador temporário consulta o GPIO23 a cada 50 µs até observar HIGH. O relatório /atuador inclui recepção e ação no relógio do ESP32, com level=1. Essa confirmação é elétrica e simulada; não é aferição acústica.

Filtro, histerese, saída e alerta autônomo mantêm a lógica de Monitor.h. O comando de teste acrescenta demonstração da atuação pela internet. A frequência continua usando tone(); o observador é desligado após o primeiro HIGH, evitando um timer de alta frequência permanente.

## Correlação de relógios

Não se subtrai UTC do receptor do uptime do Wokwi. Cada sonda registra envio no computador (H0), recepção no ESP32 (D1), resposta no ESP32 (D2) e recepção no computador (H3). Usam-se H=(H0+H3)/2 e D=(D1+D2)/2. Os pontos imediatamente antes e depois de cada evento definem interpolação linear local de D para H. O computador usa perf_counter_ns(); UTC serve à rastreabilidade.

As latências unidirecionais são estimativas que pressupõem caminhos aproximadamente simétricos nas sondas e relação local aproximadamente linear entre os relógios. A meia ida e volta interpolada é apresentada como margem de correlação aproximada, não como intervalo de confiança estatístico. Ela não inclui calibração completa da variação da velocidade do simulador. Quando a margem supera a estimativa, não se deve interpretar o resultado como medição precisa de poucos milissegundos. A ida e volta da confirmação também foi preservada, mas não usada como se fosse apenas a ida.

## Resultados

| Medida | Sensor → recepção (ms), estimativa | Comando → GPIO (ms), estimativa | Recepção local → GPIO (ms) |
|---:|---:|---:|---:|
| 1 | 199,9 | 411,4 | 8,959 |
| 2 | 263,2 | 420,9 | 10,231 |
| 3 | 253,8 | 443,4 | 7,327 |
| 4 | 325,2 | 378,0 | 11,453 |
| Média | 260,5 | 413,4 | 9,493 |

A margem média de correlação foi de aproximadamente 358,9 ms no sensor e 335,2 ms no atuador; os valores individuais estão no CSV/JSON. A precisão é limitada pela correlação temporal e pelo gateway público.

Houve quatro identificadores distintos por componente, HIGH em todos os acionamentos e sondas anteriores/posteriores a cada medida. O primeiro lembrete autônomo do quarto ciclo ocorreu aos 60,009 s simulados, métrica separada das latências.

## Integridade

As tentativas iniciais verificaram acesso e sobrecarga de um timer permanente; não entram nas médias. A execução definitiva é execucao-03-9fd31c. JSONL, ZIP da fonte, hashes e capturas são preservados. As medidas vêm dos registros instrumentados, não da diferença entre números em capturas isoladas.

Não há Blynk. A implementação usa Wi-Fi/TCP/IP e MQTT 3.1.1 em broker público, porta 1883 e QoS 0.

## Regerar os gráficos e diagramas

Instale Pillow e execute na raiz (os recortes usam as capturas originais preservadas):

~~~sh
python -m pip install -r requirements-figuras.txt
python scripts/gerar_figuras.py . dados/coletas/2026-11-05-tempos-resposta/execucao-03-9fd31c
~~~

A média local não arredondada é 9,4925 ms, apresentada como 9,493 ms com arredondamento decimal convencional.

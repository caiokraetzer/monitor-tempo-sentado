# Reprodução e instalação

## Wokwi pelo navegador

1. Crie um projeto **ESP32 Arduino** em [wokwi.com](https://wokwi.com/). O projeto parte da concepção física documentada em [MONTAGEM.md](MONTAGEM.md); esta etapa reproduz sua lógica virtualmente.
2. Copie o conteúdo de `firmware/ChairMonitor/ChairMonitor.ino` para o arquivo `sketch.ino` do Wokwi.
3. Adicione os arquivos `config.h` e `Monitor.h` ao projeto, preservando nomes e conteúdo.
4. Substitua `diagram.json` pelo diagrama do repositório. Adicione `libraries.txt` com `HX711 Arduino Library@0.7.5` e `PubSubClient@2.8`, ou use o gerenciador de bibliotecas para instalar essas versões.
5. Inicie com o sensor em 0 kg. Aguarde a mensagem de tara concluída e a telemetria com `estado: livre`. Não coloque carga durante a tara.
6. Clique no sensor HX711 e altere a carga em kg. Use 20 kg para representar ocupação e 0 kg para ausência. Não use o modelo de 5 kg, pois o fator do firmware foi especificado para o modelo de 50 kg.
7. Abra o monitor serial em 115200 baud. O log apresenta tópico e JSON. Para comprovar comunicação, observe também o recebimento no Node-RED ou coletor, e não apenas o log local.
8. Salve o projeto e copie o link real gerado pelo Wokwi para os documentos da entrega. Este repositório não inventa um link de simulação ainda não salvo.

## PlatformIO e Wokwi no VS Code

Instale Python e a extensão PlatformIO, ou use o CLI:

```sh
python -m pip install platformio==6.1.18
pio run -e esp32dev
```

Os caminhos do `wokwi.toml` apontam para esse ambiente. A extensão Wokwi utiliza o diagrama da raiz. Para usar o perfil `prolongado`, compile `pio run -e prolongado` e ajuste ambos os caminhos do TOML para `.pio/build/prolongado/`.

Para placa real, consulte a montagem e configure `local_config.h` conforme abaixo; somente depois conecte a placa e utilize `pio run -e esp32dev -t upload`. Não carregue o perfil de simulação em uma cadeira esperando uma calibração física válida.

## Node-RED e painel

Instale Node.js 20 ou superior e npm. No terminal, a partir da raiz:

```sh
cd node-red
npm install
npm start
```

O script usa `flows.json` fornecido e mantém o editor restrito a `127.0.0.1`. Abra o editor em `http://127.0.0.1:1880`. Se houver alterações pendentes, clique **Deploy**. O nó MQTT deve exibir conexão com o broker. O painel está em `http://127.0.0.1:1880/dashboard/cadeira`.

Para uma instalação Node-RED já existente, instale `@flowfuse/node-red-dashboard` no gerenciador de paleta, importe `node-red/flows.json` e implante. O caminho relativo `data/mqtt.jsonl` é resolvido pelo diretório de trabalho do processo Node-RED. Use o procedimento `npm start` acima para obter o caminho documentado.

O client ID do Node-RED é gerado automaticamente; o do ESP32 contém sufixo aleatório. Não fixe o mesmo ID para duas conexões. Caso duplique o projeto para outro dispositivo, altere o prefixo em `config.h`, `process-message.js` e no nó MQTT, gere o fluxo novamente e passe o novo prefixo ao coletor.

## Coleta e reprodução dos dados

Para registrar do broker, execute o coletor em outro terminal na raiz:

```sh
python -m pip install -r requirements.txt
python scripts/collect_mqtt.py --seconds 180
```

Em seguida execute o cenário em `dados/entradas/cenario_demonstracao.csv`, repetindo cada caso formal cinco vezes quando produzir resultados para o artigo. O relógio do cenário é o da simulação. Anote quando a carga foi realmente alterada: a interação manual pode diferir do plano. Preserve JSONL, CSV, metadados e capturas. O painel usa o relógio do receptor para o eixo temporal; eventos usam `uptime_ms` para avaliação da lógica local.

## Perfil físico

Crie `firmware/ChairMonitor/local_config.h` localmente, sem enviá-lo ao GitHub:

```cpp
#define SIMULATION 0
#define WIFI_SSID "SSID_DA_REDE"
#define WIFI_PASSWORD "SENHA_DA_REDE"
#define SCALE_FACTOR 12345.0f // exemplo: SUBSTITUIR pelo valor realmente calibrado
#define REMINDER_MS 1800000UL
```

O fator pode ser negativo conforme a orientação elétrica. Calibre com carga de referência conhecida; não use o valor ilustrativo acima nem o fator virtual 420 como calibração física. A tara automática usa as dez primeiras leituras e exige cadeira vazia. Em falha posterior, a tara original é preservada e o ciclo só rearma com carga filtrada baixa por 2 s. Reiniciar com carga sobre o sensor invalida o procedimento de tara.

## Problemas comuns

| Situação | Conferência |
|---|---|
| Painel sem dados | Mesmo prefixo, broker/porta, fluxo implantado, Wi-Fi e disponibilidade do broker. |
| Buzzer não toca | Tempo contado desde `inicio`, saída não confirmada, perfil de 60 s e volume do navegador. |
| Sensor indisponível | DT/SCK, amostras válidas, tara inicial e assento vazio para rearmar. |
| Estado ocupado com objeto | Limitação esperada: carga não identifica pessoa. |
| CSV do painel incompleto | Limite de 200 eventos; use o arquivo JSONL ou coletor para preservar toda a execução. |
| Coletor sem mensagens | Inicie ESP32 e coletor simultaneamente; telemetria/eventos não são retidos; broker público pode falhar. |

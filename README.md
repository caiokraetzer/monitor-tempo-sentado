# Monitoramento do tempo sentado com IoT para incentivo a pausas

[![Validação](https://github.com/caiokraetzer/monitor-tempo-sentado/actions/workflows/validate.yml/badge.svg)](https://github.com/caiokraetzer/monitor-tempo-sentado/actions/workflows/validate.yml)

Repositório: https://github.com/caiokraetzer/monitor-tempo-sentado

Projeto acadêmico da disciplina **Objetos Inteligentes Conectados — Universidade Presbiteriana Mackenzie**.

**Autores:** Caio Henrique Hahnemann de Souza Kraetzer e Wallace Rodrigues de Santana.

O projeto concebe um dispositivo físico instalado em uma cadeira, com **ESP32, célula de carga/HX711 e buzzer**, e fornece os arquivos para reproduzir sua lógica no **Wokwi**. O ESP32 transmite estados e eventos pela internet via **MQTT**; um painel **Node-RED** apresenta os dados e permite exportar os eventos.

## Estado desta versão

O código, os arquivos de montagem e os procedimentos de reprodução estão incluídos. Consulte [VALIDACAO.md](docs/VALIDACAO.md) para saber exatamente quais verificações foram executadas. **Esta versão não contém resultados de execução do circuito no Wokwi, ensaios físicos ou vídeo gravado.** Os CSVs de entrada e o JSON ilustrativo são identificados como sintéticos. A presença deste repositório não substitui a demonstração com MQTT exigida na entrega final.

## Conteúdo

| Caminho | Conteúdo |
|---|---|
| `firmware/ChairMonitor/` | Firmware Arduino C++, configuração, lógica, bibliotecas e diagrama Wokwi. |
| `platformio.ini` | Compilação para ESP32; perfis de 60 s e 1.800 s. |
| `diagram.json`, `wokwi.toml` | Montagem da raiz e configuração para Wokwi no VS Code. |
| `node-red/flows.json` | Fluxo importável com MQTT, validação, painel e gravação JSONL. |
| `node-red/process-message.js`, `dashboard.vue` | Fontes legíveis do processamento e da interface do painel. |
| `dados/` | Entradas sintéticas, exemplo de payload, dicionário e destino das coletas. |
| `scripts/` | Coleta MQTT, exportação CSV, geração do fluxo e validação estrutural. |
| `tests/` | Testes da lógica C++, processamento do painel e exportação. |
| `docs/` | Montagem física, comunicação, reprodução, testes, [documentação do código](docs/CODIGO.md) e [correspondência com a avaliação](docs/CRITERIOS_AVALIACAO.md). |
| `.github/workflows/validate.yml` | Automação de testes e compilação ESP32 após publicação no GitHub. |

## Executar a demonstração

1. Reproduza o circuito seguindo [EXECUCAO.md](docs/EXECUCAO.md). No Wokwi, use o modelo de ESP32 DevKit V1 e os arquivos de `firmware/ChairMonitor/`.
2. Mantenha a carga do HX711 em **0 kg** durante a inicialização e a tara. Aguarde o estado `livre` no monitor serial.
3. Inicie o Node-RED:

   ```sh
   cd node-red
   npm install
   npm start
   ```

4. Acesse o editor em `http://127.0.0.1:1880`, confirme que o fluxo está implantado e abra `http://127.0.0.1:1880/dashboard/cadeira`.
5. Ajuste a carga no Wokwi para **20 kg**. Após a confirmação e o filtro, começa um ciclo. No perfil padrão, o lembrete ocorre **60 s após a confirmação de ocupação**. Mantenha **0 kg por mais de 10 s** para encerrar; o filtro pode acrescentar alguns décimos de segundo entre a mudança da entrada e o início dessa janela.
6. Exporte os eventos pelo botão do painel. O fluxo grava todas as mensagens válidas recebidas em `node-red/data/mqtt.jsonl`. Para gerar CSV completo a partir desse arquivo, execute na raiz:

   ```sh
   python scripts/export_csv.py node-red/data/mqtt.jsonl dados/coletas/ensaio-01.csv
   ```

Como alternativa de coleta independente do painel:

```sh
python -m pip install -r requirements.txt
python scripts/collect_mqtt.py --seconds 180
```

O coletor apenas assina tópicos e registra mensagens; **não simula publicações do ESP32**. Ver [DICIONARIO.md](dados/DICIONARIO.md) para interpretar os arquivos.

## Parâmetros e MQTT

| Parâmetro | Valor |
|---|---|
| Sensor / atuador | HX711 DT GPIO19, SCK GPIO18; buzzer GPIO23 com resistor de 100 Ω. |
| Amostragem | Aproximadamente 100 ms; média móvel de cinco amostras válidas. |
| Entrada | Carga filtrada ≥10 kg durante 2 s. |
| Saída | Carga filtrada ≤5 kg durante 10 s. |
| Lembrete | 60 s no perfil de teste; 1.800 s no perfil prolongado. |
| Som | 2 kHz; três pulsos de 200 ms separados por 200 ms. Repetição a cada 60 s. |
| Broker | `broker.hivemq.com:1883`, MQTT 3.1.1, QoS 0, sem TLS/autenticação. |
| Prefixo | `mack/ods3/7c92a1/cadeira01`. |
| Tópicos | `/telemetria`, `/evento`, `/status`. Apenas `status` é retido. |
| Telemetria / reconexão | A cada 5 s; telemetria também nas transições. Reconexão a cada 5 s. |
| Painel desatualizado | Mais de 15 s sem telemetria válida. |

O broker é público e compartilhado: envie somente dados sintéticos, sem senha pessoal ou identificação de participantes. O prefixo evita colisões acidentais; não impede acesso de terceiros. Eventos perdidos não são recuperados. A tarefa de rede é separada da leitura e do aviso local. Em falha do sensor por mais de 2 s, o sistema entra em `indisponivel`, suspende o buzzer e exige assento vazio por 2 s para rearmar.

## Verificar o código

Requer Node.js 20 ou superior, Python 3.10 ou superior e, para os testes nativos, compilador C++11.

```sh
node --test tests/dashboard.test.cjs
python -m unittest discover -s tests -p "test_*.py" -v
node scripts/validate.cjs
g++ -std=c++11 -Wall -Wextra -Werror tests/test_monitor.cpp -o test-monitor
./test-monitor
python -m pip install platformio==6.1.18
pio run -e esp32dev -e prolongado
```

No Windows, execute `test-monitor.exe` no lugar de `./test-monitor`. Após alterar `process-message.js`, `dashboard.vue` ou o diagrama interno, rode `node scripts/build-flow.cjs` e verifique novamente. A compilação e os testes nativos não comprovam comunicação MQTT ou funcionamento no Wokwi; a validação integrada está em [PLANO_TESTES.md](docs/PLANO_TESTES.md).

## Relação com a entrega

A correspondência dos itens do repositório exigidos no item 2.1 da rubrica está em [CRITERIOS_AVALIACAO.md](docs/CRITERIOS_AVALIACAO.md). As responsabilidades das funções, a arquitetura e os estados estão em [CODIGO.md](docs/CODIGO.md).

Este repositório reúne fonte e dados de entrada necessários à reprodução. O [roteiro de entrega](docs/ENTREGA.md) identifica as evidências que precisam acompanhar artigo, vídeo e dados efetivamente coletados. O artigo existente ainda descreve implementação e ensaios como previstos; sua redação só deve ser atualizada para resultados após execução comprovada.

A solução se relaciona ao ODS 3 pelo incentivo à percepção da permanência prolongada no assento. Ela detecta carga, não identifica pessoas, não avalia postura e não fornece diagnóstico ou comprovação de eficácia clínica. O intervalo de 30 min é um parâmetro de engenharia, sem caráter de prescrição de saúde.

## Referências técnicas

- [HX711 no Wokwi](https://docs.wokwi.com/parts/wokwi-hx711).
- [Rede Wi-Fi do ESP32 no Wokwi](https://docs.wokwi.com/guides/esp32-wifi).
- [Biblioteca HX711](https://github.com/bogde/HX711).
- [Biblioteca PubSubClient](https://github.com/knolleary/pubsubclient).
- [FlowFuse Dashboard](https://dashboard.flowfuse.com/).
- [MQTT 3.1.1 — OASIS](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html).

Código e documentação fornecidos para avaliação acadêmica. Não é concedida licença aberta adicional nesta versão; dependências preservam suas próprias licenças.

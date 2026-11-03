# Contrato MQTT

Broker `broker.hivemq.com`, porta TCP 1883, MQTT 3.1.1, QoS 0. Wi-Fi virtual `Wokwi-GUEST`, sem senha, canal 6. Keep alive 15 s; sessão limpa; reconexão a cada 5 s. Sem TLS ou autenticação, exclusivo para demonstração com dados sintéticos.

Prefixo: `mack/ods3/7c92a1/cadeira01`.

| Tópico | Payload | Retenção |
|---|---|---|
| `/telemetria` | `{"estado":"ocupado","ocupado":true,"tempo_s":60,"alerta":true,"uptime_ms":68000}` | Não. |
| `/evento` | `{"tipo":"lembrete","tempo_s":60,"uptime_ms":68000}` | Não. |
| `/status` | Texto `online` ou `offline`. Última vontade `offline`. | Sim. |

O payload acima é ilustrativo, não uma coleta. Os eventos possíveis são `inicio`, `fim` e `lembrete`. Na indisponibilidade: `estado="indisponivel"`, `ocupado=null`, `tempo_s=0`, `alerta=false`.

A aquisição e o buzzer executam fora da tarefa de rede. O código mantém a telemetria mais recente e uma fila volátil curta de eventos para desacoplar tarefas. Eventos são descartados enquanto desconectado; não há armazenamento persistente, confirmação de entrega ou reconstrução do histórico. Overflow da fila gera aviso serial. Um envio com sucesso não garante recebimento pelo painel.

O status retido pode permanecer `online` enquanto o broker ainda não detectou uma desconexão. Por isso o painel também marca dados desatualizados após 15 s. Reinício do ESP32 perde o ciclo; queda do uptime limpa o gráfico. A volta do contador de 32 bits também limpa o gráfico; a lógica local utiliza subtração sem sinal para continuar seus intervalos.

O Node-RED recebe payload em UTF-8 e faz conversão JSON dentro da função de validação, sem tentar interpretar `online`/`offline` como JSON. Ele verifica campos, tipos e coerência dos estados antes de registrar ou atualizar a interface. O coletor independente preserva payloads estranhos para investigação.

## Camadas e módulos de comunicação

| Camada/interface | Componente e configuração | Papel no projeto |
|---|---|---|
| Acesso à rede | Wi-Fi integrado do ESP32; rede virtual Wokwi-GUEST no simulador | Obtém acesso IP para alcançar o broker remoto. |
| Transporte pela internet | TCP, porta 1883 do broker | Transporta a sessão MQTT entre clientes e servidor. |
| Protocolo de aplicação | MQTT 3.1.1, publicação/assinatura | Distribui telemetria, eventos e disponibilidade por tópico. |
| Formato das mensagens | JSON em UTF-8 para telemetria/eventos; texto para status | Define o contrato entre firmware, painel e coletor. |
| Receptor | Cliente MQTT do Node-RED, com ID automático distinto do ESP32 | Assina o prefixo e entrega mensagens à função de validação. |
| Coleta independente | Cliente Python paho-mqtt | Registra mensagens recebidas e data UTC em JSONL/CSV. |
| Apresentação | Node-RED local e FlowFuse Dashboard | Disponibiliza os indicadores ao navegador do avaliador. |

ESP32 e Node-RED iniciam conexões ao mesmo broker na internet; não precisam de conexão direta entre si. A presença de um painel em localhost não torna o caminho ESP32 → broker remoto → Node-RED uma comunicação exclusivamente local.

O contrato implementado publica dados de monitoramento; não há assinatura de comandos no ESP32 ou controle remoto do buzzer pelo navegador. Esse limite está declarado para que a documentação corresponda ao software. A demonstração deve mostrar o recebimento remoto das mensagens, além das linhas impressas no serial.

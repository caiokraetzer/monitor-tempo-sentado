# Origem e significado dos dados

| Arquivo/campo | Significado |
|---|---|
| `entradas/cenario_demonstracao.csv` | Estímulos sintéticos planejados; intervalos em segundos de simulação, ajustar a carga manualmente. Não contém medições. |
| `exemplos/telemetria.json` | Payload ilustrativo retirado da especificação do artigo; não recebido de um dispositivo. |
| `coletas/<execução>/mqtt.jsonl` | Uma linha por mensagem efetivamente recebida pelo coletor. |
| `recebido_em` | Data/hora UTC do computador receptor; não é relógio do ESP32. |
| `topic` | Tópico completo MQTT. |
| `estado` | `livre`, `ocupado` ou `indisponivel`. |
| `ocupado` | Booleano; `null` em indisponibilidade do sensor. |
| `tempo_s` | Segundos do ciclo desde a confirmação de entrada. Inclui confirmação de saída; zero quando livre/indisponível. |
| `alerta` | Verdadeiro após o primeiro lembrete até o encerramento/falha. Não significa som contínuo. |
| `uptime_ms` | Relógio de 32 bits do ESP32; reinicia no boot e dá a volta após aproximadamente 49,7 dias. |
| `tipo` | Evento `inicio`, `fim` ou `lembrete`. No fim, `tempo_s` é a duração encerrada. |
| `status` | `online`/`offline` no tópico retido. Auxiliar: não substitui a verificação de telemetria recente. |

MQTT usa QoS 0: perdas são possíveis. O coletor preserva inclusive mensagens incompatíveis em JSONL; a conversão acusa formato incompatível. O painel rejeita mensagens inválidas. Identifique possíveis mensagens de terceiros: o broker é público, sem autenticação. Nenhum dado corresponde a um participante humano ou a avaliação clínica.

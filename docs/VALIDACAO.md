# Estado da verificação

Verificações executadas em 03/11/2026. [Execução aprovada no GitHub Actions](https://github.com/caiokraetzer/monitor-tempo-sentado/actions/runs/41670980138).

Código validado: `b614691f435973e5872d3ebded219c7e14faefc6`.

| Verificação | Resultado |
|---|---|
| Processamento do painel: telemetria, rejeição de mensagens, indisponibilidade, eventos/status e reinício | 5 testes automatizados aprovados localmente e no GitHub. |
| Exportação JSONL para CSV, prevenção de sobrescrita e entrada inválida | 2 testes automatizados aprovados localmente e no GitHub. |
| Sintaxe JSON, funções do fluxo, conexões e sincronização dos arquivos gerados | Aprovado no Windows e no Linux. |
| Lógica C++ nativa, compartilhada com o firmware | 8 casos x 5 repetições: 40 cenários aprovados no GitHub, incluindo histerese, confirmação, lembretes, saída, falha e volta do contador. |
| Compilação ESP32 — perfil de teste (60 s) | Aprovada com PlatformIO. |
| Compilação ESP32 — perfil prolongado (1.800 s) | Aprovada com PlatformIO. |
| Arquivos publicados | 35 arquivos conferidos por hash após a publicação inicial. |
| Instalação e execução integrada do Node-RED | Não executada; funções verificadas isoladamente. |
| Wokwi, MQTT do dispositivo e ensaios físicos | Não executados. |

Os binários e arquivos ELF dos dois perfis estão disponíveis no artefato `firmware-esp32` da execução indicada. Artefatos do GitHub têm prazo de retenção; o fonte e a configuração permitem recompilá-los.

As versões do PlatformIO, plataforma ESP32 e bibliotecas do firmware estão fixadas. As dependências npm usam intervalos e não há lockfile, pois a instalação do painel ainda não foi executada.

Os dados de entrada e o JSON ilustrativo são sintéticos e não constituem resultados experimentais. Os testes nativos executam a lógica C++ com entradas controladas, sem placa, sensor, áudio ou broker. A compilação não comprova funcionamento elétrico ou comunicação MQTT.

A execução integrada deve seguir [PLANO_TESTES.md](PLANO_TESTES.md), preservando JSONL/CSV, capturas e identificação da versão. Não há vídeo, ensaio com pessoas ou eficácia clínica demonstrada nesta versão.

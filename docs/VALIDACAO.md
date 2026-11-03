# Estado da verificação

Verificações locais executadas em 03/11/2026:

| Verificação | Resultado |
|---|---|
| Processamento do painel: telemetria, rejeição de mensagens, indisponibilidade, eventos/status e reinício | 5 testes automatizados aprovados. |
| Exportação JSONL para CSV, prevenção de sobrescrita e entrada inválida | 2 testes automatizados aprovados. |
| Sintaxe JSON, funções do fluxo, conexões e sincronização dos arquivos gerados | Aprovado. |
| Lógica C++ nativa (8 casos x 5 repetições) | Teste incluído, execução pendente por falta de compilador C++ nesta preparação. |
| Compilação do ESP32 nos dois perfis | Workflow configurado; execução pendente após publicação no GitHub. |
| Instalação e execução integrada do Node-RED | Não executada; funções verificadas isoladamente. |
| Wokwi, MQTT do dispositivo e ensaios físicos | Não executados. |

Repositório de publicação: https://github.com/caiokraetzer/monitor-tempo-sentado. Consulte o GitHub Actions para o estado atual das verificações executadas após o envio.

Dependências de firmware fixadas no PlatformIO; dependências npm usam intervalos e não há lockfile, pois a instalação ainda não foi executada. Não declarar a compilação ou execução integrada aprovadas antes de consultar os resultados efetivos.

Os dados de entrada e o JSON ilustrativo são sintéticos e não constituem resultados experimentais. Não há vídeo, ensaio com pessoas ou eficácia clínica demonstrada nesta versão.

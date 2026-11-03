# Registros coletados

Ainda não há coletas do Wokwi ou do hardware nesta versão. Os arquivos de entrada e o payload ilustrativo estão em pastas próprias e não são resultados experimentais.

Execute `python scripts/collect_mqtt.py --seconds 180` durante a simulação. O coletor cria uma pasta com data UTC e identificador, contendo JSONL, metadados e CSV quando as mensagens puderem ser convertidas. Não sobrescreve execuções anteriores.

Adicione à pasta um `ensaio.md` com origem (Wokwi/hardware), perfil, versão do código, horário, cargas aplicadas, caso/repetição, falhas e comparação entre esperado e observado. Inclua somente resultados efetivamente observados. Não use o horário de recebimento para medir o atraso do alarme: a referência é `uptime_ms` do dispositivo.

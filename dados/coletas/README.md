# Coletas de execução

A execução integrada de **03/11/2026** está em [2026-11-03-wokwi-mqtt](2026-11-03-wokwi-mqtt/): 132 mensagens recebidas por cada um dos dois assinantes, com JSONL, CSV, metadados, eventos e análise. Veja [RESULTADOS_WOKWI.md](../../docs/RESULTADOS_WOKWI.md) para a interpretação.

Os dados completos incluem duas sessões de diagnóstico e a sessão com o diagrama corrigido. O recorte da sessão corrigida não substitui os arquivos completos. As cargas foram simuladas; a transmissão e o recebimento das mensagens ocorreram na execução.

Para uma nova coleta, execute `python scripts/collect_mqtt.py --seconds 180` durante a simulação. O coletor cria uma pasta com data UTC e identificador, sem sobrescrever execuções anteriores. Acrescente um relato com origem, perfil, commit, cargas aplicadas, casos executados, falhas e comparação entre esperado e observado.

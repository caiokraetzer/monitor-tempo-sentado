# Coleta de tempos de resposta

A execução usada nas tabelas e gráficos é **execucao-03-9fd31c**. Ela contém quatro detecções do sensor, quatro comandos/ações do buzzer, sondas de correlação temporal, captura MQTT, análise, CSV, capturas de tela e ZIP da fonte realmente executada.

Os arquivos na raiz e em execucao-02 são diagnósticos preliminares, não utilizados nas médias: uma tentativa interrompida e uma instrumentação com timer de observação permanente. O ajuste definitivo usa observador temporário e preserva a geração sonora por tone(). Consulte docs/TEMPOS_RESPOSTA.md.

As entradas de carga são sintéticas do Wokwi; mensagens, ações e horários foram coletados da execução, não fabricados por um publicador de telemetria.

# Avaliação funcional e coleta de evidências

Os critérios abaixo são metas da especificação, não resultados obtidos. Cada caso integrado deve ser repetido **cinco vezes**, mantendo registros da versão, carga, horário, monitor serial e mensagens do receptor. Use o perfil de 60 s para a avaliação inicial.

| Caso | Estímulo | Critério |
|---|---|---|
| Livre | Após tara, 0 kg por 30 s. | Livre, contagem zero, sem buzzer. |
| Entrada | 20 kg por mais de 2 s. | Exatamente um `inicio` após 2 s acima do limiar filtrado. |
| Histerese | Após ocupar, variar 6–9 kg. | Mantém ciclo ocupado. |
| Alívio breve | 0 kg por 3 s e retorno a 20 kg. | Sem `fim`; mesmo ciclo. |
| Alerta | Manter 20 kg até completar 60 s de ciclo. | `lembrete`, alerta ativo, três pulsos de 200 ms a 2 kHz; meta de erro inicial ≤0,5 s no relógio simulado. |
| Repetição | Continuar ocupado por mais 60 s. | Novo grupo de três pulsos; sem som contínuo. |
| Saída e retorno | 0 kg por mais de 10 s e retorno a 20 kg. | Um `fim`, zera/silencia; um novo `inicio` após confirmação. |
| Comunicação | Observar serial, broker e receptor. | Tópicos e campos coerentes; contabilizar mensagens recebidas e faltantes. |
| Falha de rede | Interromper acesso Wi-Fi/broker mantendo ocupado. | Contagem/aviso local preservados; painel desatualiza; retoma estado atual ao reconectar, sem recuperar histórico. |
| Falha do sensor | Suspender leituras por >2 s, restabelecer ainda carregado, depois esvaziar. | Indisponível, ocupado nulo, sem buzzer; não rearma carregado; rearma após cinco amostras e vazio por 2 s. |

Os 2 s e 10 s se aplicam à **carga filtrada**. Registre tanto a mudança da carga aplicada quanto a confirmação: o filtro adiciona tempo de resposta. No `fim`, a duração inclui a janela de saída. Não substitua essa duração pelo último valor mostrado no painel, que atualiza periodicamente.

Para falhas no Wokwi, quando a interface não permitir desconectar durante a execução, faça ensaios separados com rede/broker indisponível e com DT sem amostras, documentando o método e a limitação. Uma inicialização sem rede não equivale a comprovar recuperação de uma queda durante um ciclo.

## Registro por repetição

Crie um relato com: caso; número da repetição; origem Wokwi/hardware; commit; perfil; instante planejado e observado; eventos e duração; erro de tempo; disparos indevidos; falhas de rede; resultado aprovado/reprovado; caminho de JSONL/CSV/capturas. Registre também os casos que não puderam ser executados.

Não trate testes nativos de C++ como ensaios no simulador. Eles verificam a lógica compartilhada com entradas controladas, sem sensor, placa, áudio, Wi-Fi ou broker. A compilação verifica compatibilidade de fonte, não o comportamento elétrico.

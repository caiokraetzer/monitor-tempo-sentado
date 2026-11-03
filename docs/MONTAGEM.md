# Concepção física e adaptação virtual

O dispositivo foi concebido para instalação física. O Wokwi reproduz a lógica elétrica e a comunicação, sem validar estrutura mecânica, capacidade real ou precisão do conjunto.

| Material | Quantidade | Especificação |
|---|---:|---|
| ESP32 DevKit | 1 | Wi-Fi 2,4 GHz; alimentação USB 5 V; sinais lógicos 3,3 V. |
| Célula de carga | 1 | Ponte completa, quatro fios, referência física 200 kg. Dimensionar a estrutura junto ao sensor. |
| HX711 | 1 | Módulo físico com VCC analógico e VDD digital separados. |
| Buzzer piezoelétrico passivo | 1 | Baixa corrente, compatível com sinal 3,3 V. |
| Resistor | 1 | 100 Ω, 1/4 W, em série com o buzzer. |
| Protoboard | 1 | Aproximadamente 400 pontos; somente para o circuito. |
| Jumpers, cabo USB e fixadores | 1 conjunto | Alimentação, dados e referência de terra; fixação adequada ao sensor. |

| Origem | Destino | Observação |
|---|---|---|
| ESP32 VIN/5V | HX711 VCC | Alimentação analógica. |
| ESP32 3V3 | HX711 VDD | Módulo físico especificado; ausente no modelo virtual. |
| ESP32 GND | HX711 GND e buzzer negativo | Terra comum. |
| HX711 DT | GPIO19 | Dados. |
| HX711 SCK | GPIO18 | Relógio. |
| GPIO23 | Resistor 100 Ω → buzzer positivo | Atuador sonoro. |
| Célula | HX711 E+, E−, A+, A− | Consultar a pinagem do fabricante; cores não são universais. |

Instalar a célula entre a base e uma placa de apoio do assento, com transmissão de carga conforme o fabricante. Apoios paralelos não devem desviar toda a força do sensor. O dimensionamento e a montagem mecânica precisam ser verificados antes de uso humano; a protoboard não sustenta carga. O firmware utiliza a carga apenas para inferir ocupação, sem finalidade de pesagem corporal.

No Wokwi, o componente integrado `wokwi-hx711` representa a célula e o módulo. Usa-se o modelo de 50 kg, estímulos de 0 a 20 kg no roteiro e fator inicial 420 unidades/kg. O modelo físico de 200 kg requer calibração própria. O diagrama não constitui evidência de montagem real.

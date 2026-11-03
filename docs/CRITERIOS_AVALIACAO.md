# Correspondência com os critérios do projeto final

Revisão documental em 03/11/2026, baseada nos critérios fornecidos pelo professor. Esta correspondência facilita localizar as evidências; não atribui nota e não substitui a avaliação.

## Item 2.1 — Repositório e documentação (até 2,0 pontos)

| Critério fornecido | Localização | Situação documental e limite |
|---|---|---|
| Breve descrição do funcionamento e uso para reprodução | [README](../README.md) e [EXECUCAO.md](EXECUCAO.md) | Presente: objetivo, comportamento, montagem virtual, instalação, execução e coleta. Reprodução integrada ainda precisa ser executada e evidenciada. |
| Software desenvolvido e documentação de código | [Firmware](../firmware/ChairMonitor/), [Node-RED](../node-red/), [scripts](../scripts/) e [CODIGO.md](CODIGO.md) | Presente: fontes, funções, entradas/saídas, estados, arquitetura, dependências, configuração e limites. |
| Hardware: plataformas, sensores, atuadores e peças/caixas quando aplicáveis | [MONTAGEM.md](MONTAGEM.md) e [diagrama](../diagram.json) | Presente para o circuito proposto e sua reprodução virtual: materiais, especificações, pinagem e adaptações. Não há caixa ou peça impressa desenvolvida; não há cotas de mecânica construída. A instalação física é conceitual e seu detalhamento mecânico permanece pendente. |
| Hardware: plataformas e sensores | [MONTAGEM.md](MONTAGEM.md) | Presente: ESP32, célula de carga/HX711 e distinção entre referência física e modelo virtual. Este item se sobrepõe à linha anterior da rubrica. |
| Interfaces, protocolos e módulos de comunicação | [MQTT.md](MQTT.md), [CODIGO.md](CODIGO.md) e [MONTAGEM.md](MONTAGEM.md) | Presente: Wi-Fi integrado, DT/SCK, GPIO do buzzer, USB/serial, TCP/IP, MQTT, broker, tópicos, payloads, QoS, retenção, reconexão e destinatários. |

A simulação utiliza os arquivos fornecidos; não foram construídas peças de impressão 3D nem uma caixa. A rubrica menciona esses itens como componentes da descrição do hardware utilizado. Não foram inventadas dimensões ou arquivos de peças não desenvolvidas. Caso sejam acrescentados à montagem final, a documentação deve incluir seus modelos, medidas e arquivos correspondentes.

## Requisito básico — Internet e MQTT

O firmware implementa publicação MQTT por Wi-Fi/TCP/IP para um broker remoto; o Node-RED e o coletor assinam os tópicos desse broker. O contrato atual é de monitoramento, sem comando remoto para o ESP32.

A documentação e a compilação mostram a implementação prevista, mas **a execução integrada com MQTT ainda não foi comprovada nesta versão**. A evidência deve permitir observar o dispositivo publicando e um receptor recebendo pela internet. O log serial isolado não é prova de entrega no broker.

A rubrica estabelece que o descumprimento do requisito básico de internet/MQTT limita a nota a um quarto do total. Não é possível concluir que esse requisito foi demonstrado somente pelos testes nativos e pela compilação.

## Artigo, vídeo e acesso

| Exigência | Providência |
|---|---|
| URL do GitHub inserida adequadamente no artigo | Usar https://github.com/caiokraetzer/monitor-tempo-sentado no texto do artigo, com identificação clara de que contém documentação e fonte. A publicação deste guia não insere automaticamente esse link no Word. |
| Vídeo-demonstração no YouTube, até 3,0 pontos | Gravar a implementação e seu funcionamento, incluindo o caminho MQTT, publicar e inserir o link real no artigo. Pendente nesta versão. |
| Apresentação da implementação | Executar o roteiro e preservar evidências do protótipo simulado. |
| Dados do projeto | Entradas sintéticas e exemplo estão identificados em `dados/`; acrescentar mensagens realmente coletadas, metadados e relato da execução. |
| Acesso do avaliador | O repositório é público; conferir o acesso ao vídeo e aos links que forem inseridos no artigo. |

Segundo a rubrica, a ausência de vídeo, repositório ou ambos resulta em nota zero do projeto. Ter um repositório público e documentado atende a uma parte da entrega; ainda é necessário apresentar a implementação e inserir os links adequadamente no artigo.

Os critérios da seção 1 — introdução, materiais e métodos, resultados, conclusões e referências ABNT — são avaliados no artigo. Os arquivos deste repositório podem fornecer material para essas seções, mas não substituem sua redação e verificação no documento final. O fluxograma e a arquitetura de [CODIGO.md](CODIGO.md) também podem apoiar a descrição do software no artigo.

## Evidências disponíveis

As verificações efetivamente executadas estão em [VALIDACAO.md](VALIDACAO.md): testes do painel/exportação, 40 cenários nativos da lógica e compilação ESP32 nos dois perfis. Elas não representam ensaios Wokwi, avaliação física ou benefícios clínicos.

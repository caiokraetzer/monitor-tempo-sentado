# Correspondência com os critérios do projeto final

Revisão documental atualizada em 05/11/2026, baseada nos critérios fornecidos pelo professor. Esta correspondência facilita localizar as evidências; não atribui nota e não substitui a avaliação.

## Item 2.1 — Repositório e documentação (até 2,0 pontos)

| Critério fornecido | Localização | Situação documental e limite |
|---|---|---|
| Breve descrição do funcionamento e uso para reprodução | [README](../README.md) e [EXECUCAO.md](EXECUCAO.md) | Presente: objetivo, comportamento, montagem virtual, instalação, execução e coleta. Reprodução integrada exploratória executada; [relato e evidências](RESULTADOS_WOKWI.md). |
| Software desenvolvido e documentação de código | [Firmware](../firmware/ChairMonitor/), [Node-RED](../node-red/), [scripts](../scripts/) e [CODIGO.md](CODIGO.md) | Presente: fontes, funções, entradas/saídas, estados, arquitetura, dependências, configuração e limites. |
| Hardware: plataformas, sensores, atuadores e peças/caixas quando aplicáveis | [MONTAGEM.md](MONTAGEM.md) e [diagrama](../diagram.json) | Presente para o circuito proposto e sua reprodução virtual: materiais, especificações, pinagem e adaptações. Não há caixa ou peça impressa desenvolvida; não há cotas de mecânica construída. A instalação física é conceitual e seu detalhamento mecânico permanece pendente. |
| Hardware: plataformas e sensores | [MONTAGEM.md](MONTAGEM.md) | Presente: ESP32, célula de carga/HX711 e distinção entre referência física e modelo virtual. Este item se sobrepõe à linha anterior da rubrica. |
| Interfaces, protocolos e módulos de comunicação | [MQTT.md](MQTT.md), [CODIGO.md](CODIGO.md) e [MONTAGEM.md](MONTAGEM.md) | Presente: Wi-Fi integrado, DT/SCK, GPIO do buzzer, USB/serial, TCP/IP, MQTT, broker, tópicos, payloads, QoS, retenção, reconexão e destinatários. |

A simulação utiliza os arquivos fornecidos; não foram construídas peças de impressão 3D nem uma caixa. A rubrica menciona esses itens como componentes da descrição do hardware utilizado. Não foram inventadas dimensões ou arquivos de peças não desenvolvidas. Caso sejam acrescentados à montagem final, a documentação deve incluir seus modelos, medidas e arquivos correspondentes.

## Requisito básico — Internet e MQTT

O firmware implementa publicação MQTT por Wi-Fi/TCP/IP para um broker remoto; o Node-RED e o coletor assinam os tópicos desse broker. O contrato de monitoramento foi ampliado com comando MQTT de teste para o buzzer e instrumentação de latências.

**A execução integrada com MQTT foi evidenciada em 03/11/2026:** o ESP32 simulado publicou no HiveMQ remoto, e o Node-RED e um assinante Python registraram 132 mensagens cada. Os arquivos e a análise estão em [RESULTADOS_WOKWI.md](RESULTADOS_WOKWI.md). O ensaio inclui um ciclo encerrado e um novo início; não representa toda a campanha de cinco repetições.

A rubrica estabelece que o descumprimento do requisito básico de internet/MQTT limita a nota a um quarto do total. Neste repositório, a evidência de comunicação vem dos JSONL/CSV recebidos do broker e da execução do receptor, além dos testes nativos e da compilação.

## Artigo, vídeo e acesso

| Exigência | Providência |
|---|---|
| URL do GitHub inserida adequadamente no artigo | Inserida no Word revisado, na seção Resultados, identificando fonte, documentação e dados: https://github.com/caiokraetzer/monitor-tempo-sentado. |
| Vídeo-demonstração no YouTube, até 3,0 pontos | Gravar a implementação e seu funcionamento, incluindo o caminho MQTT, publicar e inserir o link real no artigo. Pendente nesta versão. |
| Apresentação da implementação | Demonstração exploratória simulada e coleta concluídas; registrar e publicar o vídeo exigido. |
| Dados do projeto | Entradas sintéticas identificadas e mensagens realmente recebidas, metadados e relato publicados em [RESULTADOS_WOKWI.md](RESULTADOS_WOKWI.md). |
| Acesso do avaliador | O repositório é público; conferir o acesso ao vídeo e aos links que forem inseridos no artigo. |

Segundo a rubrica, a ausência de vídeo, repositório ou ambos resulta em nota zero do projeto. Ter um repositório público e documentado atende a uma parte da entrega; o vídeo deverá ser acrescentado antes da submissão.

Os critérios da seção 1 — introdução, materiais e métodos, resultados, conclusões e referências ABNT — são avaliados no artigo. Essas seções foram revisadas no Word final, com resultados, referências citadas e diagramas atualizados. O fluxograma e a arquitetura de [CODIGO.md](CODIGO.md) também podem apoiar a descrição do software no artigo.

## Evidências disponíveis

As verificações efetivamente executadas estão em [VALIDACAO.md](VALIDACAO.md): testes do painel/exportação, 40 cenários nativos da lógica e compilação ESP32 nos dois perfis. A execução Wokwi com recepção MQTT foi acrescentada em [RESULTADOS_WOKWI.md](RESULTADOS_WOKWI.md). Nenhuma dessas verificações representa avaliação física ou comprovação de benefícios clínicos.

## Complemento de 05/11/2026 — item 7

Foram feitas quatro medições por componente, calculadas as médias e gerados gráficos a partir dos registros reais da execução instrumentada. Evidências: [TEMPOS_RESPOSTA.md](TEMPOS_RESPOSTA.md) e [execução definitiva](../dados/coletas/2026-11-05-tempos-resposta/execucao-03-9fd31c/). O método relata a margem de correlação dos relógios. O vídeo oral com identificação e rosto do aluno permanece como ação do autor antes da submissão final.

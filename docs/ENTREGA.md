# Repositório na entrega final

A exigência compartilhada do professor define o conjunto **artigo + vídeo-demonstração do funcionamento com MQTT + repositório contendo dados e código-fonte**. O artigo deve manter os requisitos das etapas anteriores. Este repositório atende à preparação do código e dos dados para reprodução; a comprovação integrada depende da execução e das evidências.

| Item | Onde está / ação necessária |
|---|---|
| Fonte ESP32 | `firmware/ChairMonitor/`. |
| Montagem simulada e bibliotecas | `diagram.json`, `libraries.txt`, `platformio.ini`, `wokwi.toml`. |
| MQTT e painel | `node-red/flows.json`, fontes do painel e `docs/MQTT.md`. |
| Instruções de reprodução | `README.md`, `docs/EXECUCAO.md` e `docs/MONTAGEM.md`. |
| Dados | Entradas sintéticas e exemplo identificados em `dados/`; acrescentar as coletas efetivas em `dados/coletas/`. |
| Verificação do código | Testes e workflow; consultar o estado efetivo em `docs/VALIDACAO.md` e no GitHub Actions. |
| Simulação publicada | Após executar e salvar, registrar o link real do Wokwi no README e artigo. |
| Vídeo com MQTT | Ainda não gravado; mostrar circuito, estados, buzzer, publicação e recebimento remoto. Inserir o link real no artigo e README. |
| Artigo final | Revisão em documento separado; não modificar a afirmação de testes previstos sem evidências. Inserir URL real do repositório. |

## Roteiro sugerido para a demonstração

Mostre brevemente os componentes e as conexões, o código e o prefixo MQTT. Inicie o Node-RED e o circuito com carga zero. Aplique 20 kg e mostre `inicio`, tempo e estado no receptor. Demonstre uma retirada breve sem encerrar, o primeiro lembrete e o buzzer, depois a retirada sustentada com `fim`. Mostre o CSV/JSONL efetivamente coletado. Se acelerar ou editar o vídeo, explique o recorte e preserve os registros originais.

Antes da submissão, abra os links de repositório, vídeo e simulação em sessão sem login ou confirme o acesso exigido pelo professor. A existência dos arquivos não garante acesso externo se o repositório estiver privado.

As orientações completas de todas as avaliações não estavam disponíveis nesta sessão; este roteiro usa os requisitos compartilhados e o artigo atual. Não presume exigências adicionais nem declara aprovação integral da entrega final.

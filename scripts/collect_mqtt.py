"""Coleta mensagens MQTT reais recebidas, sem publicar dados ou comandar o dispositivo."""
import argparse
import datetime as dt
import json
import time
import uuid
from pathlib import Path
from export_csv import convert

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=int, default=180)
    parser.add_argument('--output', default='dados/coletas')
    parser.add_argument('--broker', default='broker.hivemq.com')
    parser.add_argument('--prefix', default='mack/ods3/7c92a1/cadeira01')
    args = parser.parse_args()
    if args.seconds <= 0:
        parser.error('--seconds precisa ser positivo')
    import paho.mqtt.client as mqtt
    run_id = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:6]
    folder = Path(args.output) / run_id
    folder.mkdir(parents=True, exist_ok=False)
    source = folder / 'mqtt.jsonl'
    counts = {'mensagens': 0, 'payloads_nao_json': 0}
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    with source.open('x', encoding='utf-8') as out:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='cadeira-coleta-' + uuid.uuid4().hex[:12], protocol=mqtt.MQTTv311)
        def on_connect(c, userdata, flags, reason_code, properties):
            if reason_code == 0:
                c.subscribe(args.prefix + '/+', qos=0)
                print('Conectado; aguardando mensagens do dispositivo.')
            else:
                print(f'Falha na conexão MQTT: {reason_code}')
        def on_message(c, userdata, msg):
            text = msg.payload.decode('utf-8', errors='replace')
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                payload = text
                if text not in ('online', 'offline'):
                    counts['payloads_nao_json'] += 1
            record = {'recebido_em': dt.datetime.now(dt.timezone.utc).isoformat(), 'topic': msg.topic, 'payload': payload}
            out.write(json.dumps(record, ensure_ascii=False) + '\n')
            out.flush()
            counts['mensagens'] += 1
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect_async(args.broker, 1883, 15)
        client.loop_start()
        try:
            deadline = time.monotonic() + args.seconds
            while time.monotonic() < deadline:
                time.sleep(0.2)
        except KeyboardInterrupt:
            pass
        finally:
            client.disconnect()
            client.loop_stop()
    metadata = {'inicio_utc': started, 'fim_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                'broker': args.broker, 'porta': 1883, 'prefixo': args.prefix, 'qos': 0,
                'origem': 'mensagens recebidas pelo coletor MQTT; identificar Wokwi ou hardware no relato do ensaio', **counts}
    (folder / 'metadados.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if counts['mensagens']:
        try:
            convert(source, folder / 'mqtt.csv')
        except (ValueError, TypeError) as exc:
            print(f'JSONL preservado; CSV interrompido por mensagem incompatível: {exc}')
    print(f'Coleta salva: {folder} ({counts["mensagens"]} mensagens).')
    if not counts['mensagens']:
        raise SystemExit('Nenhuma mensagem recebida: esta coleta não comprova funcionamento do protótipo.')

if __name__ == '__main__':
    main()

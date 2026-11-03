"""Executa Node-RED e coleta MQTT real para uma demonstracao Wokwi manual."""
import argparse
import collections
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from export_csv import convert

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def load_lines(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=int, default=900)
    parser.add_argument("--output", default="integration-capture")
    args = parser.parse_args()
    import paho.mqtt.client as mqtt

    folder = (ROOT / args.output).resolve()
    folder.mkdir(parents=True, exist_ok=False)
    prefix = "mack/ods3/7c92a1/cadeira01"
    started = utc()
    record_path = folder / "mqtt-receptor.jsonl"
    node_path = ROOT / "node-red/data/mqtt.jsonl"
    metadata = {
        "origem": "Wokwi web -> broker.hivemq.com:1883 -> Node-RED e cliente paho independentes",
        "wokwi_url": "https://wokwi.com/projects/479686134986460161",
        "inicio_utc": started, "fonte_commit": os.environ.get("GITHUB_SHA"),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
        "prefixo": prefix, "broker": "broker.hivemq.com", "porta": 1883,
        "qos": 0, "perfil_lembrete_ms": 60000,
        "estimulos": "cargas sinteticas alteradas manualmente no HX711 virtual",
        "mensagens": "recebidas do broker; este script nao publica dados",
        "retencao": "status pode ser retido; telemetria e eventos nao",
        "metodo": "demonstracao integrada exploratoria; nao equivale a cinco repeticoes de todos os casos"
    }
    events = collections.Counter()
    complete_at = None
    connected_at = None
    last_progress = time.monotonic()
    nr_log = (folder / "node-red.log").open("w", encoding="utf-8")
    proc = subprocess.Popen(
        ["node", str(ROOT / "node-red/node_modules/node-red/red.js"),
         "--userDir", str(ROOT / "node-red"), "flows.json"],
        cwd=ROOT / "node-red", stdout=nr_log, stderr=subprocess.STDOUT
    )
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
        client_id="cadeira-validacao-" + uuid.uuid4().hex[:12], protocol=mqtt.MQTTv311)
    with record_path.open("x", encoding="utf-8") as output:
        def on_connect(c, userdata, flags, reason_code, properties):
            nonlocal connected_at
            print("MQTT_CONNECT", str(reason_code), utc(), flush=True)
            if reason_code == 0:
                connected_at = utc()
                c.subscribe(prefix + "/+", qos=0)
        def on_message(c, userdata, msg):
            nonlocal complete_at
            raw = msg.payload.decode("utf-8", errors="replace")
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = raw
            row = {"recebido_em": utc(), "topic": msg.topic, "payload": payload,
                   "payload_utf8": raw, "retain": bool(msg.retain), "qos": msg.qos}
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
            output.flush()
            print("MQTT_RECEBIDO " + json.dumps(row, ensure_ascii=False), flush=True)
            if msg.topic == prefix + "/evento" and isinstance(payload, dict):
                events[payload.get("tipo", "desconhecido")] += 1
                if events["inicio"] >= 2 and events["fim"] >= 1 and events["lembrete"] >= 1:
                    complete_at = time.monotonic()
        client.on_connect = on_connect
        client.on_message = on_message
        try:
            deadline = time.monotonic() + 60
            while True:
                if proc.poll() is not None:
                    raise RuntimeError("Node-RED encerrou antes da coleta")
                try:
                    with urllib.request.urlopen("http://127.0.0.1:1880/dashboard/cadeira", timeout=3) as response:
                        body = response.read()
                        metadata["dashboard_http_status"] = response.status
                        metadata["dashboard_html_sha256"] = hashlib.sha256(body).hexdigest()
                        if response.status == 200:
                            break
                except Exception:
                    if time.monotonic() >= deadline:
                        raise RuntimeError("Painel Node-RED nao respondeu em 60 s")
                    time.sleep(1)
            print("NODE_RED_HTTP_READY", utc(), flush=True)
            client.connect_async("broker.hivemq.com", 1883, 15)
            client.loop_start()
            deadline = time.monotonic() + args.seconds
            print("CAPTURE_READY", utc(), flush=True)
            while time.monotonic() < deadline:
                if proc.poll() is not None:
                    raise RuntimeError("Node-RED encerrou durante a coleta")
                if complete_at is not None and time.monotonic() - complete_at >= 10:
                    break
                if time.monotonic() - last_progress >= 30:
                    print("CAPTURE_PROGRESS", utc(), dict(events), flush=True)
                    last_progress = time.monotonic()
                time.sleep(0.2)
        finally:
            client.disconnect()
            client.loop_stop()
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            nr_log.close()

    raw_records = load_lines(record_path)
    nr_records = load_lines(node_path)
    (folder / "node-red.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in nr_records), encoding="utf-8")
    convert(record_path, folder / "mqtt-receptor.csv")
    convert(folder / "node-red.jsonl", folder / "node-red.csv")
    metadata.update({"fim_utc": utc(), "conectado_utc": connected_at,
        "mensagens_paho": len(raw_records), "mensagens_node_red": len(nr_records),
        "eventos_paho": dict(events)})
    (folder / "metadados.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    accepted_events = collections.Counter(row["payload"].get("tipo") for row in nr_records
        if row["topic"] == prefix + "/evento" and isinstance(row["payload"], dict))
    checks = {
        "dashboard_respondeu_http_200": metadata.get("dashboard_http_status") == 200,
        "paho_recebeu_telemetria": any(row["topic"] == prefix + "/telemetria" for row in raw_records),
        "node_red_recebeu_telemetria": any(row["topic"] == prefix + "/telemetria" for row in nr_records),
        "node_red_recebeu_inicio": accepted_events["inicio"] >= 2,
        "node_red_recebeu_fim": accepted_events["fim"] >= 1,
        "node_red_recebeu_lembrete": accepted_events["lembrete"] >= 1,
        "node_red_recebeu_alerta_ativo": any(isinstance(row["payload"], dict) and row["payload"].get("alerta") is True for row in nr_records)
    }
    (folder / "verificacoes.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Conteudo preservado nos logs e no artefato; facilita inspecao via API sem alterar os dados.
    for path in sorted(folder.glob("*")):
        if path.suffix in (".json", ".jsonl", ".csv", ".log"):
            print("BEGIN_CAPTURE_FILE " + path.name, flush=True)
            print(path.read_text(encoding="utf-8-sig"), end="", flush=True)
            print("\nEND_CAPTURE_FILE " + path.name, flush=True)
    print("CAPTURE_RESULT", json.dumps(checks), flush=True)
    if not all(checks.values()):
        raise SystemExit("Execucao integrada incompleta; dados observados foram preservados.")

if __name__ == "__main__":
    main()

"""Converte registros JSONL recebidos pelo Node-RED em CSV, sem dependências."""
import argparse
import csv
import json
from pathlib import Path

FIELDS = ['recebido_em', 'topic', 'estado', 'ocupado', 'tempo_s', 'alerta', 'uptime_ms', 'tipo', 'status']

def convert(source, target):
    count = 0
    with Path(source).open(encoding='utf-8-sig') as src, Path(target).open('x', newline='', encoding='utf-8') as dst:
        writer = csv.DictWriter(dst, fieldnames=FIELDS)
        writer.writeheader()
        for number, line in enumerate(src, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                payload = record['payload']
                row = {'recebido_em': record['recebido_em'], 'topic': record['topic']}
                if isinstance(payload, dict):
                    row.update({k: payload.get(k, '') for k in FIELDS[2:]})
                elif payload in ('online', 'offline'):
                    row['status'] = payload
                else:
                    raise ValueError('payload desconhecido')
                writer.writerow(row)
                count += 1
            except (KeyError, ValueError, TypeError) as exc:
                raise ValueError(f'Linha {number}: {exc}') from exc
    return count

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='JSONL gravado pelo Node-RED ou coletor')
    parser.add_argument('output', help='Novo CSV (um arquivo existente não será sobrescrito)')
    args = parser.parse_args()
    print(f'{convert(args.input, args.output)} registros exportados.')

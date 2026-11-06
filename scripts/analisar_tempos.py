"""Calcula respostas unidirecionais por correlação explícita de relógios.
O erro de sincronização é estimado conservadoramente pela meia ida-e-volta das sondas.
"""
from pathlib import Path
import json,sys,csv,bisect,statistics
folder=Path(sys.argv[1])
records=[json.loads(x) for x in (folder/'mensagens.jsonl').read_text(encoding='utf8').splitlines() if x.strip()]
tx={r['payload']['id']:r for r in records if r.get('kind')=='tx'}
probes=[];sensors=[];actions=[]
for r in records:
 if r.get('kind')!='rx' or not isinstance(r.get('payload'),dict):continue
 p=r['payload'];topic=r['topic']
 if topic.endswith('/sync') and p.get('id') in tx:
  a=tx[p['id']]
  if not a['topic'].endswith('/sync_req'):continue
  probes.append({**p,'h0_us':a['host_us'],'h3_us':r['host_us'],
   'd_us':(p['d1_us']+p['d2_us'])/2,'h_us':(a['host_us']+r['host_us'])/2,
   'rtt_us':r['host_us']-a['host_us']})
 elif topic.endswith('/sensor'):
  sensors.append({**p,'received_host_us':r['host_us'],'utc':r['utc']})
 elif topic.endswith('/atuador') and p.get('id') in tx:
  a=tx[p['id']]
  if a['topic'].endswith('/comando'):
   actions.append({**p,'sent_host_us':a['host_us'],'ack_host_us':r['host_us'],'utc':r['utc']})
probes.sort(key=lambda p:p['d_us'])
def correlate(d):
 j=bisect.bisect_right([p['d_us'] for p in probes],d)
 if j==0 or j==len(probes):raise ValueError('Faltam sondas antes/depois do evento')
 a,b=probes[j-1],probes[j]
 w=(d-a['d_us'])/(b['d_us']-a['d_us']);rate=(b['h_us']-a['h_us'])/(b['d_us']-a['d_us'])
 h=(1-w)*a['h_us']+w*b['h_us']
 uncertainty=((1-w)*a['rtt_us']+w*b['rtt_us'])/2
 return h,uncertainty,{'probe_before':a['id'],'probe_after':b['id'],'weight':w,'clock_rate_host_per_device':rate}
rows=[]
for p in sensors:
 h,u,fit=correlate(p['detected_us'])
 rows.append({'numero':p['id'],'componente':'Sensor HX711','resposta_ms':(p['received_host_us']-h)/1000,'incerteza_relogio_ms':u/1000,'origem':p,'correlacao':fit})
for p in actions:
 if p.get('level')!=1:raise ValueError('GPIO sem confirmação HIGH')
 h,u,fit=correlate(p['action_us'])
 rows.append({'numero':p['id'],'componente':'Buzzer GPIO23','resposta_ms':(h-p['sent_host_us'])/1000,'incerteza_relogio_ms':u/1000,
 'processamento_local_ms':(p['action_us']-p['received_us'])/1000,
 'ida_e_volta_confirmacao_ms':(p['ack_host_us']-p['sent_host_us'])/1000,'origem':p,'correlacao':fit})
summary={}
for name in ['Sensor HX711','Buzzer GPIO23']:
 group=[r for r in rows if r['componente']==name]
 if len(group)!=4:raise ValueError(f'{name}: esperado 4, recebido {len(group)}')
 if len({r['numero'] for r in group})!=4:raise ValueError('IDs duplicados')
 if any(r['resposta_ms']<0 for r in group):raise ValueError('Estimativa negativa: revisar correlação')
 summary[name]={'n':4,'media_ms':statistics.mean(r['resposta_ms'] for r in group),
 'incerteza_media_conservadora_ms':statistics.mean(r['incerteza_relogio_ms'] for r in group),
 'desvio_padrao_amostral_ms':statistics.stdev(r['resposta_ms'] for r in group)}
result={'metodo':'correlacao local linear entre sondas adjacentes; pontos medios dos quatro timestamps; estimativas unidirecionais',
 'sondas':len(probes),'medidas':rows,'resumo':summary,'registros':len(records)}
(folder/'analise-tempos.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
with (folder/'tempos-resposta.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['numero','componente','resposta_ms','incerteza_relogio_ms','processamento_local_ms','ida_e_volta_confirmacao_ms']);w.writeheader()
 for row in rows:w.writerow({k:row.get(k,'') for k in w.fieldnames})
print(json.dumps(result,ensure_ascii=True,indent=2))

"""Recebe MQTT real do ESP32; envia somente probes de relógio e comandos de teste.
Os valores de sensor e as confirmações GPIO são produzidos pelo firmware no Wokwi.
"""
import argparse,sys,time,json,threading,datetime,os
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlsplit
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--deps');p.add_argument('--seconds',type=int,default=900)
a=p.parse_args()
if a.deps:sys.path.insert(0,a.deps)
import paho.mqtt.client as mqtt
out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
base='mack/ods3/7c92a1/cadeira01/ensaio-9fd31c'
start=time.perf_counter_ns();lock=threading.RLock();records=[];sent={};sync=[];actions=[];sensors=[];ready=False;connected=False
def elapsed():return (time.perf_counter_ns()-start)/1000
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
f=(out/'mensagens.jsonl').open('x',encoding='utf8',buffering=1)
def record(r):
 with lock:records.append(r);f.write(json.dumps(r,ensure_ascii=False)+'\n')
def on_connect(c,u,flags,reason,properties):
 global connected
 c.subscribe('mack/ods3/7c92a1/cadeira01/#',qos=0);connected=True
 record({'kind':'conexao','utc':stamp(),'host_us':elapsed(),'reason':str(reason)})
def on_message(c,u,msg):
 global ready
 now=elapsed()
 try:payload=json.loads(msg.payload)
 except Exception:payload=msg.payload.decode('utf8',errors='replace')
 r={'kind':'rx','utc':stamp(),'host_us':now,'topic':msg.topic,'payload':payload,'retain':msg.retain}
 record(r)
 with lock:
  if msg.topic==base+'/ready':ready=True
  if msg.topic==base+'/sync' and isinstance(payload,dict) and payload.get('id') in sent:
   ready=True
   tx=sent[payload['id']]
   if tx['topic']==base+'/sync_req':
    row={**payload,'h0_us':tx['host_us'],'h3_us':now}
    row['device_mid_us']=(row['d1_us']+row['d2_us'])/2
    row['host_mid_us']=(row['h0_us']+row['h3_us'])/2
    row['rtt_ms']=(row['h3_us']-row['h0_us'])/1000
    sync.append(row)
  if msg.topic==base+'/sensor' and isinstance(payload,dict):sensors.append({**payload,'received_host_us':now,'utc':r['utc']})
  if msg.topic==base+'/atuador' and isinstance(payload,dict):
   tx=sent.get(payload.get('id'))
   if tx and tx['topic']==base+'/comando':actions.append({**payload,'sent_host_us':tx['host_us'],'ack_host_us':now,'utc':r['utc']})
def publish(kind,id):
 payload={'id':id}
 if kind=='comando':payload['acao']='teste_buzzer'
 tx={'kind':'tx','utc':stamp(),'host_us':elapsed(),'topic':base+'/'+kind,'payload':payload}
 with lock:sent[id]=tx
 record(tx);c.publish(tx['topic'],json.dumps(payload,separators=(',',':')),qos=0,retain=False)
def state():
 with lock:return {'connected':connected,'ready':ready,'sync_count':len(sync),'sensors':sensors,'actions':actions,'last':records[-14:],'sync_last':sync[-3:]}
page="""<!doctype html><html lang="pt-br"><meta charset="utf-8"><title>Coleta MQTT – Monitor de tempo sentado</title><style>body{font:17px Segoe UI,Arial;margin:36px;color:#182a38;background:#f5f7f8}h1{font-size:27px}section{background:white;padding:22px;margin:18px 0;border:1px solid #cbd4dc}table{border-collapse:collapse;width:100%}td,th{padding:9px;border-bottom:1px solid #ddd;text-align:left}pre{font-size:13px;white-space:pre-wrap}small{color:#536b7c}.ok{color:#146942}</style><h1>Monitor de tempo sentado · recepção MQTT</h1><small>ESP32/Wokwi → broker.hivemq.com:1883 → assinante Python independente</small><section id="status"></section><section><h2>Sensor HX711 · detecções recebidas</h2><table id="sensor"></table></section><section><h2>Buzzer · confirmações do GPIO23</h2><table id="act"></table></section><section><h2>Últimas mensagens reais</h2><pre id="log"></pre></section><script>async function refresh(){let s=await(await fetch('/state')).json();document.getElementById('status').innerHTML='<b class=ok>MQTT '+(s.connected?'conectado':'aguardando')+'</b> · Firmware '+(s.ready?'pronto':'aguardando')+' · Sondas de relógio: '+s.sync_count;document.getElementById('sensor').innerHTML='<tr><th>Medida</th><th>Carga (kg)</th><th>Detecção ESP32 (µs)</th><th>Recebido (UTC)</th></tr>'+s.sensors.map(x=>'<tr><td>'+x.id+'</td><td>'+x.load_kg+'</td><td>'+x.detected_us+'</td><td>'+x.utc+'</td></tr>').join('');document.getElementById('act').innerHTML='<tr><th>Comando</th><th>Recepção ESP32 (µs)</th><th>Ação GPIO (µs)</th><th>Leitura GPIO</th></tr>'+s.actions.map(x=>'<tr><td>'+x.id+'</td><td>'+x.received_us+'</td><td>'+x.action_us+'</td><td>'+x.level+'</td></tr>').join('');document.getElementById('log').textContent=s.last.map(x=>x.topic+' '+JSON.stringify(x.payload)).join('\\n')}refresh();setInterval(refresh,1000)</script></html>"""
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  value=json.dumps(state(),ensure_ascii=False).encode() if urlsplit(self.path).path=='/state' else page.encode()
  self.send_response(200);self.send_header('Content-Type','application/json; charset=utf-8' if self.path.startswith('/state') else 'text/html; charset=utf-8');self.end_headers();self.wfile.write(value)
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',8765),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
c=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id='medicao-9fd31c-'+str(int(time.time())),protocol=mqtt.MQTTv311)
c.on_connect=on_connect;c.on_message=on_message;c.connect('broker.hivemq.com',1883,keepalive=20);c.loop_start()
record({'kind':'metadados','utc':stamp(),'host_us':elapsed(),'clock':'perf_counter_ns','broker':'broker.hivemq.com:1883','run':'9fd31c','method':'sondas MQTT, relógios correlacionados por pontos médios; valores unidirecionais estimados'})
print('RECEPTOR PRONTO http://127.0.0.1:8765',flush=True)
last_probe=last_command=0;probe_id=1000;cmd_id=0
try:
 while elapsed()<a.seconds*1e6 and not (out/'parar').exists():
  now=time.monotonic()
  if connected and now-last_probe>=1.5:
   probe_id+=1;publish('sync_req',probe_id);last_probe=now
  if ready and len(sync)>=8 and cmd_id<4 and now-last_command>=4:
   cmd_id+=1;publish('comando',cmd_id);last_command=now
   print('COMANDO',cmd_id,flush=True)
  if int(now)%3==0:
   (out/'estado.json').write_text(json.dumps(state(),ensure_ascii=False,indent=2),encoding='utf8')
  time.sleep(.1)
finally:
 c.loop_stop();c.disconnect();server.shutdown()
 with lock:result={'sync':sync,'sensors':sensors,'actions':actions,'records_count':len(records)}
 (out/'coleta.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');f.close()
 print('FINAL',len(sensors),len(actions),len(sync),flush=True)

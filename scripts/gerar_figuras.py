from PIL import Image,ImageDraw,ImageFont
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
import json,sys,math
r=Path(sys.argv[1]);data=Path(sys.argv[2])
fig=r/'docs/figuras';fig.mkdir(exist_ok=True)
fontpath=next((str(p) for p in [Path('C:/Windows/Fonts/arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')] if p.exists()),'Arial.ttf');boldpath=next((str(p) for p in [Path('C:/Windows/Fonts/arialbd.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')] if p.exists()),'Arial Bold.ttf')
def font(n,b=False):return ImageFont.truetype(boldpath if b else fontpath,n)
def text(d,x,y,s,n=32,b=False,fill='black',anchor='mm'):d.multiline_text((x,y),s,font=font(n,b),fill=fill,anchor=anchor,align='center',spacing=8)
def box(d,a,s,n=33):
 d.rounded_rectangle(a,radius=15,fill='#f6f6f6',outline='#222222',width=3);text(d,(a[0]+a[2])/2,(a[1]+a[3])/2,s,n)
def arrow(d,p,both=False):
 d.line(p,fill='#222222',width=4)
 def head(a,b):
  x,y=b;ang=math.atan2(y-a[1],x-a[0]);d.polygon([(x,y),(x-15*math.cos(ang-.5),y-15*math.sin(ang-.5)),(x-15*math.cos(ang+.5),y-15*math.sin(ang+.5))],fill='#222222')
 head(p[-2],p[-1])
 if both:head(p[1],p[0])
x=json.loads((data/'analise-tempos.json').read_text(encoding='utf8'));rows=x['medidas']
# Gráfico de latências estimadas em quatro medidas e na média.
im=Image.new('RGB',(1700,980),'white');d=ImageDraw.Draw(im)
L,T,R,B=135,185,1630,785;yy=lambda y:B-(B-T)*y/600
for v in range(0,601,100):
 d.line((L,yy(v),R,yy(v)),fill='#dedede',width=2);text(d,L-38,yy(v),str(v),29)
d.line((L,T,L,B,R,B),fill='black',width=3)
colors=['#256287','#b85b35'];names=['Sensor HX711','Buzzer GPIO23'];groups=[[q for q in rows if q['componente']==name] for name in names]
for j,label in enumerate(['1','2','3','4','Média']):
 cx=280+j*285
 for k,group in enumerate(groups):
  val=group[j]['resposta_ms'] if j<4 else x['resumo'][names[k]]['media_ms']
  xp=cx+(-55 if k==0 else 55);d.rectangle((xp-41,yy(val),xp+41,B),fill=colors[k])
  text(d,xp,yy(val)-27,f'{val:.1f}'.replace('.',','),30,b=True,fill=colors[k])
 text(d,cx,B+40,label,32)
text(d,880,48,'Tempos de resposta por componente',42,True)
text(d,880,105,'Estimativas unidirecionais por correlação de relógios',32)
for k,label in enumerate(['Sensor → recepção MQTT','Comando MQTT → GPIO23']):
 xp=400+k*700;d.rectangle((xp-190,142,xp-157,166),fill=colors[k]);text(d,xp+35,155,label,29)
text(d,880,910,'Medida · valores em milissegundos',31)
text(d,880,954,'As margens de correlação são informadas na tabela e no método.',27)
im.save(data/'grafico-latencias.png',dpi=(300,300))
# Cronometragem local do atuador.
im=Image.new('RGB',(1700,820),'white');d=ImageDraw.Draw(im);L,T,R,B=140,130,1615,650;yy=lambda y:B-(B-T)*y/15
for v in [0,3,6,9,12,15]:
 d.line((L,yy(v),R,yy(v)),fill='#dddddd',width=2);text(d,L-35,yy(v),str(v),29)
d.line((L,T,L,B,R,B),fill='black',width=3)
group=groups[1];vals=[q['processamento_local_ms'] for q in group];mean=sum(vals)/4
for j,v in enumerate(vals+[mean]):
 xp=285+j*280;d.rectangle((xp-65,yy(v),xp+65,B),fill='#256287');text(d,xp,yy(v)-28,str(Decimal(str(v)).quantize(Decimal('0.001'),rounding=ROUND_HALF_UP)).replace('.',','),32,True);text(d,xp,B+37,str(j+1) if j<4 else 'Média',31)
text(d,880,48,'Resposta local do buzzer após receber o comando',40,True)
text(d,880,735,'Recepção MQTT no ESP32 → primeiro HIGH observado no GPIO23 (ms)',31)
text(d,880,788,'Diferenças no mesmo relógio do ESP32; observador nominal de 50 µs.',27)
im.save(data/'grafico-processamento-local.png',dpi=(300,300))
# Arquitetura inclui os dois sentidos MQTT e distingue o receptor de ensaio.
im=Image.new('RGB',(1800,900),'white');d=ImageDraw.Draw(im)
box(d,(20,70,550,250),'Célula de carga + HX711\nDT: GPIO19 · SCK: GPIO18',35)
box(d,(680,50,1120,280),'ESP32 DevKit\nWi-Fi integrado\nControle local + filas',35)
arrow(d,[(550,160),(680,160)])
box(d,(1270,70,1780,250),'Buzzer · GPIO23\nAlerta e comando de teste',35)
arrow(d,[(1120,160),(1270,160)])
box(d,(680,440,1120,620),'HiveMQ remoto\nTCP/IP · MQTT 3.1.1\nbroker.hivemq.com:1883',33)
arrow(d,[(900,280),(900,440)],True);text(d,1170,355,'Telemetria, eventos,\nsondas e comandos',30)
box(d,(20,440,550,620),'Node-RED\nPainel de monitoramento\nTópicos originais',33)
arrow(d,[(680,530),(550,530)])
box(d,(1270,430,1780,650),'Coletor Python\nEnvio e recepção MQTT\nRelógio monotônico e JSONL',33)
arrow(d,[(1120,530),(1270,530)],True)
text(d,900,785,'O teste remoto usa o subprefixo ensaio-9fd31c.\nSensor e alerta autônomo preservam a lógica de Monitor.h.',32)
im.save(fig/'arquitetura-mqtt-final.png',dpi=(300,300))
# Fluxo funcional da extensão de medição.
im=Image.new('RGB',(1700,1370),'white');d=ImageDraw.Draw(im)
box(d,(500,20,1200,130),'Conectar Wi-Fi e MQTT;\nassinar sondas e comandos',36)
box(d,(500,205,1200,315),'mqtt.loop(): receber mensagem',36);arrow(d,[(850,130),(850,205)])
box(d,(20,430,500,585),'Sonda de relógio:\nregistrar D1 e D2;\npublicar /sync',35)
box(d,(605,430,1095,585),'Comando teste_buzzer:\nregistrar recepção;\nenfileirar ordem local',34)
box(d,(1200,430,1680,585),'Telemetria/eventos:\nconsumir filas;\npublicar no broker',35)
for px in [260,850,1440]:arrow(d,[(850,315),(850,360),(px,360),(px,430)])
box(d,(605,680,1095,830),'Laço local:\niniciar padrão de 3 pulsos\nusando tone()/noTone()',34)
arrow(d,[(850,585),(850,680)])
box(d,(605,925,1095,1080),'Observar GPIO23;\nmarcar o primeiro HIGH;\ndesligar o observador',35)
arrow(d,[(850,830),(850,925)])
box(d,(605,1170,1095,1330),'Tarefa de rede:\npublicar /atuador\ncom ID e tempos',35)
arrow(d,[(850,1080),(850,1170)])
text(d,265,895,'Monitor.h continua\nlendo o HX711 e\nconfirmando ocupação.\n\nCada inicio também\ngera /sensor com\nID e detected_us.',34)
text(d,1440,900,'Coletor externo registra\nH0 no envio e H3\nna recepção das sondas.\n\nAs medições do sensor\ne do atuador recebem\nos horários do receptor.',33)
im.save(fig/'fluxo-mqtt-medicao.png',dpi=(300,300))
# Recortes sem alterar o conteúdo das capturas.
for name,target in [('wokwi-deteccao-3.png','captura-ocupacao.png'),('wokwi-alerta-atualizado.png','captura-alerta.png')]:
 original=Image.open(data/'capturas'/name)
 original.crop((956,40,original.width,original.height)).save(data/'capturas'/target,dpi=(160,160))
print(json.dumps({'graficos':['grafico-latencias.png','grafico-processamento-local.png'],'figuras':str(fig)},ensure_ascii=True))

#include <Arduino.h>
#include <WiFi.h>
#include <HX711.h>
#include <PubSubClient.h>
#include "config.h"
#include "Monitor.h"

HX711 scale;
long diagnosticRaw=0;
Monitor monitor(REMINDER_MS);
struct Packet { char topic[100]; char payload[220]; };
QueueHandle_t telemetryQueue, eventQueue;
bool sounding=false, soundOn=false;
uint32_t soundStart=0;
void emitPacket(bool event, const char* suffix, const char* payload);

#include <esp_timer.h>
#define MEASURE_BASE MQTT_PREFIX "/ensaio-9fd31c"
struct MeasureCommand { uint32_t id; int64_t receivedUs; };
struct MeasureAction { uint32_t id; int64_t receivedUs, actionUs; int level; };
QueueHandle_t measureCommands, measureActions;
esp_timer_handle_t measureTimer;
portMUX_TYPE measureMux = portMUX_INITIALIZER_UNLOCKED;
volatile bool measureBusy=false, measureFirst=false;
volatile int64_t measureStartedUs=0, measureReceivedUs=0;
volatile uint32_t measureId=0;
PubSubClient* measureMqtt=nullptr;
uint32_t sensorMeasureId=0;
void measureWave(void*) {
 if(!measureBusy || measureFirst) return;
 if(digitalRead(BUZZER_PIN)==HIGH){
   MeasureAction a{measureId,measureReceivedUs,esp_timer_get_time(),1};
   measureFirst=true; xQueueSend(measureActions,&a,0); esp_timer_stop(measureTimer);
 }
}
uint32_t measureParseId(const char* body){const char* p=strstr(body,"\"id\"");if(!p || !(p=strchr(p,':')))return 0;unsigned long id=strtoul(p+1,nullptr,10);return id>0 && id<=1000000000UL?(uint32_t)id:0;}
void measureCallback(char* topic,byte* bytes,unsigned int len){
 int64_t d1=esp_timer_get_time();if(len>=120 || !measureMqtt)return;char body[120];memcpy(body,bytes,len);body[len]=0;
 uint32_t id=measureParseId(body);if(!id)return;
 if(!strcmp(topic,MEASURE_BASE "/sync_req")){char response[200];int64_t d2=esp_timer_get_time();
 snprintf(response,sizeof(response),"{\"id\":%lu,\"d1_us\":%lld,\"d2_us\":%lld}",(unsigned long)id,(long long)d1,(long long)d2);
 measureMqtt->publish(MEASURE_BASE "/sync",response,false);
 }else if(!strcmp(topic,MEASURE_BASE "/comando") && strstr(body,"\"teste_buzzer\"")){MeasureCommand c{id,d1};xQueueSend(measureCommands,&c,0);}
}
void measureSubscribe(PubSubClient& mqtt){measureMqtt=&mqtt;mqtt.setCallback(measureCallback);mqtt.subscribe(MEASURE_BASE "/sync_req",0);mqtt.subscribe(MEASURE_BASE "/comando",0);mqtt.publish(MEASURE_BASE "/ready","{\"instrumentacao\":\"9fd31c\",\"sensor\":\"HX711\",\"atuador\":\"GPIO23\"}",false);Serial.println("ENSAIO 9fd31c: MQTT pronto; comando remoto e cronometros instrumentados");}
void measureNetwork(PubSubClient& mqtt){MeasureAction a;while(xQueueReceive(measureActions,&a,0)==pdTRUE){char out[220];snprintf(out,sizeof(out),"{\"id\":%lu,\"received_us\":%lld,\"action_us\":%lld,\"gpio\":23,\"level\":%d}",(unsigned long)a.id,(long long)a.receivedUs,(long long)a.actionUs,a.level);mqtt.publish(MEASURE_BASE "/atuador",out,false);Serial.printf("ENSAIO_ATUADOR %s\n",out);}}
void measureBegin(){measureCommands=xQueueCreate(4,sizeof(MeasureCommand));measureActions=xQueueCreate(8,sizeof(MeasureAction));esp_timer_create_args_t args{};args.callback=measureWave;args.name="measure-wave";if(!measureCommands || !measureActions || esp_timer_create(&args,&measureTimer)!=ESP_OK){Serial.println("ERRO INSTRUMENTACAO");while(true)delay(1000);}}
void measureLocal(){
 if(measureBusy){
   int64_t elapsed=esp_timer_get_time()-measureStartedUs;
   bool want=elapsed<1000000 && (elapsed/200000)%2==0;
   if(want!=soundOn){soundOn=want;if(want)tone(BUZZER_PIN,2000);else noTone(BUZZER_PIN);}
   if(elapsed>=1000000){measureBusy=false;esp_timer_stop(measureTimer);}
   return;
 }
 MeasureCommand c;
 if(xQueueReceive(measureCommands,&c,0)==pdTRUE){
   noTone(BUZZER_PIN);soundOn=false;
   measureId=c.id;measureReceivedUs=c.receivedUs;measureFirst=false;
   measureStartedUs=esp_timer_get_time();measureBusy=true;
   tone(BUZZER_PIN,2000);soundOn=true;esp_timer_start_periodic(measureTimer,50);
 }
}
void measureSensor(int64_t detectionUs,float kg){char out[200];snprintf(out,sizeof(out),"{\"id\":%lu,\"detected_us\":%lld,\"load_kg\":%.3f,\"estado\":\"ocupado\"}",(unsigned long)++sensorMeasureId,(long long)detectionUs,kg);emitPacket(true,"ensaio-9fd31c/sensor",out);}


void emitPacket(bool event, const char* suffix, const char* payload) {
  Packet p{};
  snprintf(p.topic,sizeof(p.topic),"%s/%s",MQTT_PREFIX,suffix);
  snprintf(p.payload,sizeof(p.payload),"%s",payload);
  Serial.printf("%s %s\n",p.topic,p.payload);
  if (event) {
    if (xQueueSend(eventQueue,&p,0)!=pdTRUE) Serial.println("AVISO: fila cheia, evento remoto descartado");
  } else xQueueOverwrite(telemetryQueue,&p);
}
void publishState(uint32_t now) {
  char json[220];
  snprintf(json,sizeof(json),"{\"estado\":\"%s\",\"ocupado\":%s,\"tempo_s\":%.3f,\"alerta\":%s,\"uptime_ms\":%lu}",
    monitor.state(),!monitor.available?"null":monitor.occupied?"true":"false",
    monitor.elapsed(now)/1000.0,monitor.alert?"true":"false",(unsigned long)now);
  Serial.printf("SENSOR raw=%ld tara=%ld carga_filtrada_kg=%.3f\n", diagnosticRaw, scale.get_offset(), monitor.load);
  emitPacket(false,"telemetria",json);
}
// Som sem delay: 200 ms ligado, 200 desligado, três pulsos.
void updateSound(uint32_t now) {
  if (measureBusy) return;
  if (!monitor.available || !monitor.occupied) sounding=false;
  uint32_t elapsed=now-soundStart;
  if (sounding && elapsed>=1000) sounding=false;
  bool wantOn=sounding && (elapsed/200)%2==0;
  if (wantOn!=soundOn) {
    soundOn=wantOn;
    if (soundOn) tone(BUZZER_PIN,2000); else noTone(BUZZER_PIN);
  }
}
// Toda operação de rede potencialmente bloqueante fica fora da aquisição/alerta.
void networkTask(void*) {
  WiFiClient socket;
  PubSubClient mqtt(socket);
  mqtt.setServer(MQTT_HOST,MQTT_PORT); mqtt.setKeepAlive(15);
  mqtt.setSocketTimeout(2); mqtt.setBufferSize(512);
  WiFi.mode(WIFI_STA);
  uint32_t retry=0; bool first=true, haveLast=false, fresh=false;
  Packet last{},p{};
  char clientId[70],statusTopic[100];
  snprintf(clientId,sizeof(clientId),"cadeira-esp32-%08lx",(unsigned long)esp_random());
  snprintf(statusTopic,sizeof(statusTopic),"%s/status",MQTT_PREFIX);
  for (;;) {
    if (xQueueReceive(telemetryQueue,&p,0)==pdTRUE) { last=p; haveLast=true; fresh=true; }
    bool connected = WiFi.status()==WL_CONNECTED && mqtt.connected();
    if (!connected && (first || uint32_t(millis()-retry)>=5000)) {
      first=false; retry=millis();
      if (WiFi.status()!=WL_CONNECTED) {
        mqtt.disconnect();
#if SIMULATION
        WiFi.begin(WIFI_SSID,WIFI_PASSWORD,6);
#else
        WiFi.begin(WIFI_SSID,WIFI_PASSWORD);
#endif
      } else {
        if (mqtt.connect(clientId,statusTopic,0,true,"offline")) {
          mqtt.publish(statusTopic,"online",true);
          measureSubscribe(mqtt);
          if (haveLast) { mqtt.publish(last.topic,last.payload,false); fresh=false; }
        }
      }
    }
    connected=WiFi.status()==WL_CONNECTED && mqtt.connected();
    if (connected) {
      mqtt.loop();
      measureNetwork(mqtt);
      // Telemetria corrente substitui a anterior; sem reconstruir histórico.
      if (fresh) { mqtt.publish(last.topic,last.payload,false); fresh=false; }
    }
    while (xQueueReceive(eventQueue,&p,0)==pdTRUE) {
      if (connected) mqtt.publish(p.topic,p.payload,false);
      // Offline: descarta. Não há armazenamento/reenvio de eventos perdidos.
    }
    vTaskDelay(pdMS_TO_TICKS(20));
  }
}
void setup() {
  Serial.begin(115200); pinMode(BUZZER_PIN,OUTPUT); noTone(BUZZER_PIN);
  measureBegin();
  telemetryQueue=xQueueCreate(1,sizeof(Packet)); eventQueue=xQueueCreate(16,sizeof(Packet));
  if (!telemetryQueue || !eventQueue) { Serial.println("ERRO: sem memoria para filas"); while(true) delay(1000); }
  scale.begin(HX_DT,HX_SCK); scale.set_scale(SCALE_FACTOR);
  Serial.println("INICIALIZACAO: mantenha o assento vazio para tara; perfil de lembrete em ms:");
  Serial.println(REMINDER_MS);
  if (xTaskCreatePinnedToCore(networkTask,"mqtt",6144,nullptr,1,nullptr,0)!=pdPASS) {
    Serial.println("ERRO: tarefa de rede indisponivel; logica local continua");
  }
}
void loop() {
  static uint32_t sampleAt=0, telemetryAt=0;
  static int tareCount=0; static int64_t tareSum=0;
  static bool calibrated=false;
  uint32_t now=millis();
  bool valid=false; float kg=0;
  if (uint32_t(now-sampleAt)>=100) {
    sampleAt=now;
    if (scale.is_ready()) {
      long raw=scale.read(); diagnosticRaw=raw; // somente quando is_ready; não usa read_average/tare bloqueantes
      if (!calibrated) {
        tareSum+=raw;
        if (++tareCount==10) {
          scale.set_offset((long)(tareSum/10)); calibrated=true;
          Serial.println("TARA CONCLUIDA: aguarde confirmacao de assento vazio");
        }
      } else { kg=(raw-scale.get_offset())/SCALE_FACTOR; valid=isfinite(kg); }
    }
  }
  bool wasAvailable=monitor.available;
  Monitor::Event event=monitor.step(now,valid,kg);
  int64_t decisionUs=esp_timer_get_time();
  if (event==Monitor::START) measureSensor(decisionUs,monitor.load);
  if (wasAvailable && !monitor.available) Serial.println("FALHA SENSOR: esvazie o assento para rearmar; ciclo anterior incerto");
  if (event!=Monitor::NONE) {
    const char* kind=event==Monitor::START?"inicio":event==Monitor::END?"fim":"lembrete";
    uint32_t duration=event==Monitor::END?monitor.endedDuration:monitor.elapsed(now);
    char json[200]; snprintf(json,sizeof(json),"{\"tipo\":\"%s\",\"tempo_s\":%.3f,\"uptime_ms\":%lu}",kind,duration/1000.0,(unsigned long)now);
    emitPacket(true,"evento",json);
    if (event==Monitor::REMINDER) { sounding=true; soundStart=now; }
  }
  if (event!=Monitor::NONE || wasAvailable!=monitor.available || uint32_t(now-telemetryAt)>=5000) {
    telemetryAt=now; publishState(now);
  }
  measureLocal(); updateSound(now); delay(10);
}

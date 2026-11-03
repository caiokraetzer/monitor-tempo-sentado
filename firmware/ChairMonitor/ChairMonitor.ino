#include <Arduino.h>
#include <WiFi.h>
#include <HX711.h>
#include <PubSubClient.h>
#include "config.h"
#include "Monitor.h"

HX711 scale;
Monitor monitor(REMINDER_MS);
struct Packet { char topic[100]; char payload[220]; };
QueueHandle_t telemetryQueue, eventQueue;
bool sounding=false, soundOn=false;
uint32_t soundStart=0;

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
  emitPacket(false,"telemetria",json);
}
// Som sem delay: 200 ms ligado, 200 desligado, três pulsos.
void updateSound(uint32_t now) {
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
          if (haveLast) { mqtt.publish(last.topic,last.payload,false); fresh=false; }
        }
      }
    }
    connected=WiFi.status()==WL_CONNECTED && mqtt.connected();
    if (connected) {
      mqtt.loop();
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
      long raw=scale.read(); // somente quando is_ready; não usa read_average/tare bloqueantes
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
  updateSound(now); delay(1);
}

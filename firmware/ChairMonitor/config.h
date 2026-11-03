#pragma once
// Arquivo local opcional, ignorado pelo Git: SSID/senha/calibração física.
#if __has_include("local_config.h")
#include "local_config.h"
#endif
#ifndef SIMULATION
#define SIMULATION 1
#endif
#ifndef REMINDER_MS
#define REMINDER_MS 60000UL
#endif
#ifndef WIFI_SSID
#define WIFI_SSID "Wokwi-GUEST"
#endif
#ifndef WIFI_PASSWORD
#define WIFI_PASSWORD ""
#endif
#ifndef SCALE_FACTOR
#if SIMULATION
#define SCALE_FACTOR 420.0f
#else
#error "Defina SCALE_FACTOR com a calibracao da celula fisica em local_config.h"
#endif
#endif
#define MQTT_HOST "broker.hivemq.com"
#define MQTT_PORT 1883
#define MQTT_PREFIX "mack/ods3/7c92a1/cadeira01"
constexpr int HX_DT=19, HX_SCK=18, BUZZER_PIN=23;

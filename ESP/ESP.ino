/*
   Self-service bike station notifier
   ESP-8266 that connects to a WiFi network and chats with an MQTT server (publish & subscribe)
   Antoine de Chassey.
*/

#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DNSServer.h>            //Local DNS Server used for redirecting all requests to the configuration portal
#include <ESP8266WebServer.h>     //Local WebServer used to serve the configuration portal
#include <WiFiManager.h>          //https://github.com/tzapu/WiFiManager WiFi Configuration Magic

// Leds
#define FASTLED_ESP8266_NODEMCU_PIN_ORDER
#include <FastLED.h>
#define NUM_LEDS 2
#define DATA_PIN 1
CRGB leds[NUM_LEDS];

const String application = "Self-service bike notifier";  // name of the application, used in the log MQTT payloads and topics

// WiFi setup
const String ssid = "ESP_" + application;
const char* password = "";
const char* client_mac;

// MQTT setup
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_username = "esp";                     // used while connecting to the broker
const char* mqtt_password = "";                        // leave empty if not needed
const char* mqtt_topic = "notifier";                   // used to fetch the coming data from the server
const char* mqtt_topic_log = "log";                    // used to log the hardware status to broker
char* mqtt_payload;
boolean retained = false;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  // Leds
  pinMode(LED_BUILTIN, OUTPUT);     // Initialize the LED_BUILTIN pin as an output
  digitalWrite(LED_BUILTIN, LOW);   // Turn the LED on (Note that LOW is the voltage level
  FastLED.addLeds<WS2811, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.clear();

  // Setup serial port
  Serial.begin(115200);

  // Setup WiFi
  WiFiManager wifiManager;
  //reset saved settings
  //wifiManager.resetSettings();
  wifiManager.autoConnect(String(ssid).c_str(), password);

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  Serial.println("Application name: "); Serial.print(application);
  Serial.println("MQTT Server: "); Serial.print(mqtt_server);
  Serial.println("MQTT Topic: "); Serial.print(mqtt_topic) ;

  client_mac = client_MAC();
  Serial.println("ESP mac: "); Serial.print(client_mac);


  // Connect to the MQTT broker and send status
  connect_MQTT();
  digitalWrite(LED_BUILTIN, HIGH);   // Turn the LED_BUILTIN off (Note that HIGH is the voltage level)
}

void loop() {
  if (!client.connected()) {
    connect_MQTT();
  }
  client.loop();
}


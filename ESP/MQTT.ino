/********** MQTT functions **********/

void connect_MQTT() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection... ");
    // Attempt to connect
    if (client.connect(client_mac, mqtt_username, mqtt_password, mqtt_topic_log, 1, 0, String("{\"name\": \"" + application + "\", \"status\": \"disconnected\"}").c_str())) {
      Serial.println("\t/!\\ connected /!\\");
      // sending log "connected" to broker
      client.publish(mqtt_topic_log, String("{\"name\": \"" + application + "\", \"status\": \"connected\"}").c_str(), retained);
      client.subscribe(mqtt_topic, 1);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// handles message arrived on subscribed topic(s)
void callback(char* topic, byte* payload, unsigned int length) {
  char json[150];
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    json[i] = (char)payload[i];
  }
  Serial.println();
  Serial.println(json);

  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.parseObject(json);
  if (!root.success()) {
    Serial.println("parseObject() failed");
    Strobe(0x99, 0xff, 0xff, 5, 50, 1000);
    return;
  }
  int bikes = root["bikes"];
  int spots = root["spots"];
  control(bikes, spots);
  Serial.println(bikes);
  Serial.println(spots);
}


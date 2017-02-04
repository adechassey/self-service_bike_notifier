#!/usr/bin/env python
# -*- coding: utf8-*-
'''
Created on 19 août 2016

@author: Antoine de Chassey
'''

from station import Station
import paho.mqtt.client as mqtt
import json, datetime, time

mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883
mqtt_topic = "notifier"

# address = "Euratechnologies, Lille" (use if you don't know the ID)
station_id = 83

def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    
def sendMQTT(station):
    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.connect(mqtt_broker, mqtt_port, 60)
    except Exception as e:
        print("[ERROR] - Could not connect to MQTT broker")
        print(e)
    else:
        payload = {}
#         payload['id'] = station.id
#         payload['name'] = station.name
#         payload['address'] = station.address
#         payload['status'] = station.status
        payload['bikes'] = station.bikes
        payload['spots'] = station.spots
#         payload['paiement'] = station.paiement
#         payload['lastupd'] = station.lastupd

        json_payload = json.dumps(payload)

        try:
            client.publish(mqtt_topic, json_payload, qos=1, retain=True)
            print("[INFO] - Publishing to " + mqtt_topic + ": " + json_payload)
            client.disconnect()
            print("[INFO] - ...done!")
        except Exception as e:
            print("[ERROR] - Could not send to MQTT broker")
            print(e)

if __name__ == "__main__":
#     history = []
#     record = {}
    station = Station()
    station.getStationByID(station_id)
#         station.getStationByGPS(address)
    if(station.id != "null"):
#             now = datetime.datetime.now()
#             record['time'] = now.strftime("%Y-%m-%d %H:%M")
#             record['bikes'] = station.bikes
#             json_record = json.dumps(record)
#             history.append(record)
#             print(history)
        station.showStation()
        sendMQTT(station)
    else:
        print("[ERROR] - Could not get station information")

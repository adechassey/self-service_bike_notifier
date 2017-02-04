#!/usr/bin/env python
# -*- coding: utf8-*-
'''
Created on 19 août 2016

@author: Antoine de Chassey
'''

import requests, xmltodict, json
from geopy.geocoders.osm import Nominatim
from math import radians, cos, sin, asin, sqrt

class Station():

    def __init__(self):
        self.id = "null"
        self.name = "null"
        self.latitude = "null"
        self.longitude = "null"
        self.address = "null"
        self.status = "null"
        self.bikes = "null"
        self.spots = "null"
        self.paiement = "null"
        self.lastupd = "null"
        
    def getStationByID(self, id_station):
        # Get id, name, latitude, longitude
        r = requests.get('http://www.vlille.fr/stations/xml-stations.aspx')
        if r.status_code == 200:
            data = r.text
            stations = json.loads(json.dumps(xmltodict.parse(data)))['markers']['marker']
#             print(stations.items())
            for station in stations:
                if(station['@id'] == str(id_station)):
                    self.id = station['@id']
                    self.name = station['@name']
                    self.latitude = station['@lat']
                    self.longitude = station['@lng']
                    break   
        else:
            r.raise_for_status()
            print('[ERROR] - Could not connect')

        # Get more details
        payload = {'borne': id_station}
        r = requests.get('http://www.vlille.fr/stations/xml-station.aspx', params=payload)
        if r.status_code == 200:
            data = r.text
            station = json.loads(json.dumps(xmltodict.parse(data)))['station']
            self.address = station['adress']
            self.status = station['status']
            self.bikes = station['bikes']
            self.spots = station['spots']
            self.paiement = station['paiement']
            self.lastupd = station['lastupd']
        else:
            r.raise_for_status()
            print('[ERROR] - could not connect')
            
                
    def getStationByGPS(self, address):
        geolocator = Nominatim()
        try:
            location = geolocator.geocode(address)
            lat1 = location.latitude
            lon1= location.longitude
            # Convert decimal degrees to radians
            lon1, lat1 = map(radians, [lon1, lat1])
        except Exception as e:
            print("[ERROR] - Could not find coordinates for this address")
            print(e)
        
        else:        
            # Get id, name, latitude, longitude
            r = requests.get('http://www.vlille.fr/stations/xml-stations.aspx')
            if r.status_code == 200:
                data = r.text
                stations = json.loads(json.dumps(xmltodict.parse(data)))['markers']['marker']
    
                bestDistance = 10000
                for station in stations:
                    lat2 = float(station['@lat'])
                    lon2 = float(station['@lng'])
                    # Convert decimal degrees to radians 
                    lon2, lat2 = map(radians, [lon2, lat2])
                    # Haversine formula 
                    dlon = lon2 - lon1 
                    dlat = lat2 - lat1 
                    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                    c = 2 * asin(sqrt(a)) 
                    distance = 6367 * c   
                    if(distance < bestDistance):
                        bestDistance = distance
                        self.id = station['@id']
                
                r = requests.get('http://www.vlille.fr/stations/xml-stations.aspx')
                if r.status_code == 200:
                    data = r.text
                    stations = json.loads(json.dumps(xmltodict.parse(data)))['markers']['marker']
                    for station in stations:
                        if(station['@id'] == str(self.id)):
                            self.id = station['@id']
                            self.name = station['@name']
                            self.latitude = station['@lat']
                            self.longitude = station['@lng']
                            break   
                else:
                    r.raise_for_status()
                    print('[ERROR] - Could not connect')
        
                # Get more details
                payload = {'borne': self.id}
                r = requests.get('http://www.vlille.fr/stations/xml-station.aspx', params=payload)
                if r.status_code == 200:
                    data = r.text
                    station = json.loads(json.dumps(xmltodict.parse(data)))['station']
                    self.address = station['adress']
                    self.status = station['status']
                    self.bikes = station['bikes']
                    self.spots = station['spots']
                    self.paiement = station['paiement']
                    self.lastupd = station['lastupd']
                else:
                    r.raise_for_status()
                    print('[ERROR] - Could not connect')
                
            else:
                r.raise_for_status()
                print('[ERROR] - Could not connect')
            
            
    def showStation(self):
        print('id: ' + self.id)
        print('name: ' + self.name)
        print('latitude: ' + self.latitude)
        print('longitude: ' + self.longitude)
        print('address: ' + self.address)
        print('status: ' + self.status)
        print('bikes: ' + self.bikes)
        print('spots: ' + self.spots)
        print('paiement: ' + self.paiement)
        print('lastupd: ' + self.lastupd)
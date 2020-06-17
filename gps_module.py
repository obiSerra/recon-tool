#!/usr/bin/env python3

import socket
import threading
import time
import re
import math

class GpsModule(threading.Thread):
    def __init__(self, dev="/dev/ttyACM0"):
        threading.Thread.__init__(self)
        self.current_val = None
    
        self.values = []
        self.stop_thread = False

    def nmea_to_dec(self, nmea_val, ind):
        fl_val = float(nmea_val)
        dd = math.floor(fl_val / 100)
        mm = fl_val - (dd * 100)
        splitted = [dd, mm]
        sig = -1 if ind == "S" or ind == "W" else 1

        return sig * (dd + mm / 60)

    def stop(self):
        self.stop_thread = True

    def update_values(self, new_value=None):
        treshold = 5
        if new_value != None:
            self.values.append(new_value)
               
        self.values = [v for v in sorted(self.values, key=lambda row: row['timestamp']) if time.time() - v['timestamp'] < treshold][:10]

        if len(self.values) == 0:
            return
        lat = 0
        lng = 0
        timestamp = 0
        
        for v in self.values:
            lat += v['lat']
            lng += v['lng']
            timestamp += v['timestamp']
        
#        print(len(self.values))
        self.current_val = {'lat': lat/len(self.values), 'lng': lng/len(self.values), 'timestamp': timestamp/len(self.values)}


    def run(self):           
        with open("/dev/ttyACM0", "r") as d:
            line = d.readline()
            while line != "":
                if self.stop_thread:
                    break
                line = d.readline()    
                if (re.search('^\$GPGLL', line)):
                    data = line.split(',')
                    lat = self.nmea_to_dec(data[1], data[2])
                    lng = self.nmea_to_dec(data[3], data[4])
                    result = {'lat': lat, 'lng': lng, 'timestamp': time.time()}
                    self.update_values(result)

                   # time.sleep(0.2)
                    


##gps = GpsModule()
##gps.run()

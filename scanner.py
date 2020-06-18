#!/usr/bin/env python3
import time
import subprocess as sp
import pandas as pd
from os import path

from gps_module import GpsModule
from wifi_scanner_module import WifiScanner


refresh_time = 5
log_shell = True
log_file = True

csv_file = 'temp.csv'

if __name__ == '__main__':
   print("[+] Starting")

   try:
      wifiScanner = WifiScanner()
      print("[+] Starting gps module")
      gps = GpsModule()
      gps.start()

      wifiScanner = WifiScanner(dev_name='wlan1', gps=gps)
      wifiScanner.start_sniffing()
      while True:
         time.sleep(refresh_time)
         networks = wifiScanner.networks
         if log_shell:
            sp.call('clear',shell=True)
            print("\n\n\n")
            print(networks)
         if log_file:
            if path.exists(csv_file):
               prev = pd.read_csv(csv_file)            
               prev = pd.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto", "Lat/Lng"])
               prev.set_index("BSSID", inplace=True)
               networks = pd.concat([prev,networks])
             
            
#            networks.drop_duplicates()
            networks.to_csv(csv_file, index=True)

      
   except:
      gps.stop()
      gps.join()
      wifiScanner.stop_sniffing()
      raise

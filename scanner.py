#!/usr/bin/env python3
import time
import re
import subprocess as sp
import sys
import pandas as pd
from os import path
from threading import Thread
import optparse

from gps_module import GpsModule
from wifi_scanner_module import WifiScanner


class Scanner(Thread):
   def __init__(self, csv_file=None, refresh_time=5):
      Thread.__init__(self)
      self.wifiScanner = WifiScanner()
      print("[+] Starting gps module")
      self.gps = GpsModule()
      self.csv_file=csv_file
      self.refresh_time=refresh_time

   def run(self):

      try:
         self.gps.start()
         self.wifiScanner = WifiScanner(dev_name='wlan1', gps=self.gps)

         self.wifiScanner.start_sniffing()

         while True:
            time.sleep(self.refresh_time)
            networks = self.wifiScanner.networks
            if self.detached == False:
               sp.call('clear',shell=True)
               print("\n\n\n")
               print(networks)
               
            if self.csv_file:
               if path.exists(self.csv_file):
                  prev = pd.read_csv(self.csv_file)            
                  # This config should be shared
                  prev = pd.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto", "Lat/Lng", "Time"])
                  prev.set_index("BSSID", inplace=True)
                  networks = pd.concat([prev,networks])
                  
               networks.to_csv(self.csv_file, index=True)                     
                  
      except (KeyboardInterrupt):
         self.gps.stop()
         self.gps.join()
         self.wifiScanner.stop_sniffing()
         raise
      


if __name__ == '__main__':
   
   parser = optparse.OptionParser('usage%prog -o <out file>')
   parser.add_option('-o', '--output', dest='outfile', type='string', help='The output file')
   parser.add_option('-r', dest='refresh_time', type='int', default=5, help='Time between refresh (default=5)')
   parser.add_option('-d', '--detach', dest='detach', action='store_true', help='Detach the process')
   parser.add_option('-k', '--kill', dest='kill', action='store_true', help='kill active scanning')
   (options, args) = parser.parse_args()

   if options.kill == True:
      ps = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE)
      active = [p.decode("utf-8") for p in ps.stdout.splitlines() if re.search("scanner.py .* SUB", p.decode("utf-8"))]
      
      for a in active:
         subprocess.run(["kill", "-9", re.split("\s+", a)[1]])

   elif options.detach != True or sys.argv[-1] == 'SUB':
      scanner = Scanner(csv_file=options.outfile, refresh_time=options.refresh_time) 
      scanner.start()
   else:
      cmd = [sys.executable]
      cmd += sys.argv
      cmd.append("SUB")
      p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)
      exit()


 



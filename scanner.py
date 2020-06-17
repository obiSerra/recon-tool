#!/usr/bin/env python3
import time

from gps_module import GpsModule
from logger_module import Logger

if __name__ == '__main__':
   print("[+] Starting")
   try:
      print("[+] Starting gps module")
      gps = GpsModule()
      logger = Logger('./temp.txt')
      gps.start()
      while True:

         if gps.current_val != None:
            logger.append_row([gps.current_val['lat'], gps.current_val['lng'], gps.current_val['timestamp']])
         
         time.sleep(3)
         ##   kill_gpsd()   


   except:
      gps.stop()
      gps.join()
      raise

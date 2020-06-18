from scapy.all import *
from threading import Thread
import pandas
import time
import os
import subprocess

from wifi_utils_module import *

class WifiScanner(Thread):
    def __init__(self, dev_name="wlan1", gps=None):
        Thread.__init__(self)
        self.ch = 1
        self.gps = gps
        self.dev_mon = ifconfig_cmd(dev_name)
        self.networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto", "Lat/Lng", "Time"])
        self.networks.set_index("BSSID", inplace=True)
        self.t = None

    def sniff_callback(self, packet):
        if packet.haslayer(Dot11Beacon):
            # extract the MAC address of the network
            bssid = packet[Dot11].addr2
            # get the name of it
            ssid = packet[Dot11Elt].info.decode()
            try:
                dbm_signal = packet.dBm_AntSignal
            except:
                dbm_signal = "N/A"
            # extract network stats
            try:
                stats = packet[Dot11Beacon].network_stats()
            except:
                stats = {}
            
            # get the channel of the AP
            channel = stats.get("channel")
            # get the crypto
            crypto = stats.get("crypto")            
            
            if self.gps and self.gps.current_val:
                position = "{},{}".format(self.gps.current_val['lat'], self.gps.current_val['lng'])
            else:
                position = '-'
            self.networks.loc[bssid] = (ssid, dbm_signal, channel, crypto, position, time.time())

    def run(self):
        while self.t and self.t.running:
            os.system(f"iwconfig {self.dev_mon} channel {self.ch}")
            self.ch = self.ch % 14 + 1
            time.sleep(0.5)

    def start_sniffing(self):
        print("[+] Starting sniffer")
        self.t = AsyncSniffer(prn=self.sniff_callback, iface=self.dev_mon, store=False)
        self.t.start()
        self.start()

##        self.change_channel()
    def stop_sniffing(self):
        if self.t:
            print("[+] Stopping sniffer")
            self.t.stop()
            self.t = None            
            

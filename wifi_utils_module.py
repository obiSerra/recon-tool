#!/usr/bin/python3
import subprocess

def airmon_cmd(dev):
    print("[+] Enabling monitor mode for {}".format(dev))
    cmd_resp = subprocess.run(["airmon-ng", "start", dev], stdout=subprocess.PIPE)
    ifconfig_cmd(dev, False)

    
def ifconfig_cmd(dev, start=True):
    # monitor device name
    devmon = "{}mon".format(dev)
    ifconfig_resp = subprocess.run(["ifconfig"], stdout=subprocess.PIPE)
    if not dev in str(ifconfig_resp):
        print("[!] {} not found".format(dev))
        # TODO should throw an exception
    elif "{}".format(devmon) in str(ifconfig_resp):
        pass
    else:
        if start:
            airmon_cmd(dev)

    return devmon
        
def main():
    ifconfig_cmd("wlan1", True)


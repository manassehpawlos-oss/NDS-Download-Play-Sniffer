import subprocess
from scapy.all import *

def find_wlan_devs():
    phy_target = 0
    options = subprocess.run(["sudo","bash","wlan_devs/airmon_options.sh"],check=True,capture_output = True)
    output = options.stdout.decode("utf-8")
 
    
    iface_dict = {}
    for i in range(10):
        phy_index = output.find(f'phy{i}')
        end_of_name_index = output[phy_index:].find("\n")
        if phy_index != -1:
            iface_dict[f'phy{i}'] = output[phy_index+5:end_of_name_index+phy_index].replace("\t","")
    return(iface_dict)

def get_wlanmon_name(dev,phy):
    subprocess.run(["sudo","bash","wlan_devs/dev_init.sh",dev],check=True,capture_output = True)
    new_name = find_wlan_devs()[phy]
    subprocess.run(["sudo","bash","wlan_devs/final_wlan_setup.sh",new_name],check=True)
    return new_name

def get_phy_from_wlan(device,dictionary):
    for phy,dev in dictionary.items():
        if device == dev:
            return phy
    return "Failed to find device" #should never reach this state.


def phy_extractor(option,dictionary):
    for key in dictionary:
        if option.find(key) != -1:
            return key
    return "Ah, didn't find the key."

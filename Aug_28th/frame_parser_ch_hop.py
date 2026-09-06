from scapy.all import *
#from PIL import Image, ImageTk
import timeit
from tkinter import *
from tkinter import ttk
import subprocess

from ads.frame_fcts import *



beacon_value_uniqueID = bytes.fromhex("0009BF000A00000001")
radiotap_length = int(36)

def frame_processor(ad_list, packet):
    packet_raw = raw(packet)[radiotap_length:] 
    start_of_data = packet_raw.find(beacon_value_uniqueID)
    frame_freq = packet.ChannelFrequency #actually not necessary
    
    if start_of_data != -1:
        if has_proper_CRC(packet_raw):
            frame_info_printer(packet_raw,start_of_data)
            frag_is_claimed = False
            for advert in ad_list:
                if advert.frame_processor_and_claimer(packet, packet_raw, start_of_data):
                    frag_is_claimed = True #only necessary for troubleshooting
                    break
            if not frag_is_claimed:
                print("frame unclaimed. Should never happen.")
        else:
            print("NDS, corrupted message")
    else:
        pass
    #stop = timeit.default_timer()
    #print('Time (ms): ', int(1000*1000*(stop - start))/1000)
def channel_hopper(root, ad_list, current_channel):
    ad_on_this_channel = -1
    new_channel = current_channel
    
    for ad in ad_list:
        #print(F"Troubleshooting - currently tested ad has ID {ad.ID}")
        if ad.occupied_channel == current_channel and ad.is_assembled is False:
            ad_on_this_channel = ad.ID
            #print(f'Troubleshooting - Ad {ad.ID} is on THIS channel!')
            break
        else:
            #print(f'Troubleshooting - Ad {ad.ID} is on channel {ad.occupied_channel}')
            pass
    #print(f"Troubleshooting - Flag is set to {ad_on_this_channel}")
    
    if ad_on_this_channel != -1:
        print(f"-----Object {ad_on_this_channel} still assembling, will remain on channel {current_channel}")
    else:
        new_channel = (current_channel+6)%18
        print(f"-----------Hopping from channel {current_channel} to {new_channel}")
        subprocess.run(["sudo", "iw", "wlan0mon", "set", "channel", str(new_channel)],
                       check=True, stdout = subprocess.DEVNULL)
        root.update_idletasks()        
    return new_channel
#----------------------------------------------
#total length = 228
#atheros header length = 36

def start_sniff(dev_name):
   sniff = AsyncSniffer(iface=dev_name, count = 0,
                        filter = "less 250 && greater 200" +
                        "&& wlan broadcast") 
   sniff.start()
   return sniff

def initialize_wifi_card(initial_channel):
    subprocess.run(["sudo", "bash", "./bash_scripts/9271_init.sh",str(initial_channel)],check=True)

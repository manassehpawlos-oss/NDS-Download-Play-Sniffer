from tkinter import *
from tkinter import ttk
from scapy.all import *
from PIL import Image, ImageTk

from frame_parser_ch_hop import *
from ads.advert_class import *
from disp.disp_update_fcts import *
from disp.disp_class import *


first_waiting_period = 500
loop_waiting_period = 500
channel_hop_period = int(loop_waiting_period/2)
initial_channel = 1
troubleshooting_period = 1000



class Scan_window:
    def __init__(self,root,top_mainframe):
        self.root = root
        root.title("Test display")
        mainframe = ttk.Frame(top_mainframe)
        mainframe.grid(column = 0, row = 0,sticky=(N, W, E, S))
        mainframe.grid_forget()
        
        #----------objects below
        self.ad_list = generate_ad_list(4)
        self.disp_list = generate_disp_list(mainframe, 4)
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(1, weight=1)

        self.start_button_default_text = "Start button"
        self.start_button = ttk.Button(mainframe,
                                       command = self.first_scan,
                                       text = self.start_button_default_text)
        self.start_button.grid(column = 0, row = 2, sticky = (N,W,E,S))
        
        self.stop_button_default_text = "Stop button"
        self.stop_button = ttk.Button(mainframe,
                                      command = self.cancel,
                                      text = self.stop_button_default_text)
        self.stop_button.grid(column = 1, row = 2, sticky = (N,W,E,S))
        self.mainframe = mainframe #shouldn't have to use self. in init now

        #------other values below
        self.current_channel = initial_channel #change def later
        self.scanloop_ID = 0
        self.hopper_ID = 0
        self.dev_name = "N/A"
    def cancel(self):
        self.stop_button["text"] = "Stopping..."
        self.start_button["text"] = self.start_button_default_text
        
        self.root.after_cancel(self.scanloop_ID)
        self.root.after_cancel(self.hopper_ID) #add cancelling everything
        for disp in self.disp_list:
            reset(disp)
        for ad in self.ad_list:
            initialize(ad)
        self.stop_button["text"] = "Stopped!"
        subprocess.run(["sudo","systemctl","start","NetworkManager"],check=True)
        self.root.update_idletasks()
    def first_scan(self):
        self.start_button["text"] = "Scanning..."
        self.stop_button["text"] = self.stop_button_default_text
        sniff = start_sniff(self.dev_name) #should add fct here, or split up entire fct
                                #into 1st iteration, and following it's.
        self.scanloop_ID = self.root.after(first_waiting_period,
                                           lambda:
                                           self.subsequent_scan(sniff))        
        self.hopper_ID = self.root.after(channel_hop_period,
                   self.channel_hop_caller)

    def subsequent_scan(self,sniff):
        packet_list = sniff.stop()
        sniff = start_sniff(self.dev_name)
        self.scanloop_ID = self.root.after(loop_waiting_period,
                                           lambda:
                                           self.subsequent_scan(sniff)) 
    
        if bool(packet_list) is True:
            for packet in packet_list:
                frame_processor(self.ad_list,packet)
                self.root.update_idletasks()
        else:
            print("No frames captured, skipping processing")
            
        display_ads(self.ad_list,self.disp_list)
        update_ads(self.ad_list,self.disp_list)

    def channel_hop_caller(self):
        "Relies on external function for logic"
        self.current_channel = channel_hopper(self.root, self.ad_list, self.current_channel)
        self.root.update_idletasks()
        self.hopper_ID = self.root.after(channel_hop_period, self.channel_hop_caller)            


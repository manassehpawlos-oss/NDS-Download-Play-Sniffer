from tkinter import *
from tkinter import ttk
import subprocess
import re

from options_window.initial_screen_class import *
from options_window.options_fetcher import *
from scan_window import *

class Main_window:
    def __init__(self,root):
        self.root = root
        top_mainframe = ttk.Frame(root)
        top_mainframe.grid(column = 0, row = 0,sticky=(N, W, E, S))
        s = ttk.Style()
        s.theme_use('clam')
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        top_mainframe.columnconfigure(0, weight=1)
        top_mainframe.rowconfigure(0, weight=1)
        
        self.chosen_dev = ""
        self.options_window = Options_window(root,top_mainframe)
        self.options_window.start_button["command"] = self.attempt_selection
        self.options_dict = self.options_window.options_dict
        #self.scan_window = Scan_window(root,top_mainframe)
        
        self.scan_window = Scan_window(root,top_mainframe)
        
        self.top_mainframe = top_mainframe
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    def attempt_selection(self, *args):
        if self.options_window.selection_check() is True:
            selected_option = self.options_window.selection_accepted()
            selected_phy = phy_extractor(selected_option,self.options_dict)
            selected_wlan = self.options_dict[selected_phy]
            self.scan_window.dev_name = get_wlanmon_name(selected_wlan,selected_phy)
            self.scan_window.mainframe.grid()            
        else:
            self.options_window.selection_rejected()
    
    def open_scan_window(self,*args):
        self.options_window.initialize()
    
    def on_close(self, *args):
        if self.options_window.killwifi_state.get() == True:
            subprocess.run(["sudo","systemctl","start","NetworkManager"],stdout = subprocess.DEVNULL)
        if self.scan_window.dev_name != "N/A":
            subprocess.run(["sudo",'airmon-ng','stop',str(self.scan_window.dev_name)],
                           stdout = subprocess.DEVNULL)
        self.root.destroy()
        

root = Tk()
Main_window(root)
root.mainloop()
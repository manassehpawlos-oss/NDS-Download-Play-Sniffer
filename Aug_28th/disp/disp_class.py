from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def generate_disp_list(mainframe, number):
    disp_list = []
    for i in range(number):
        disp_list.append(Display(mainframe, (i+1)))
    return disp_list
    
def default_entries_loader(display):
    for entry,default in display.default_dict.items():
        if isinstance(default,str):
            entry["text"] = default
        else:
            entry["image"] = default

class Display:
    def __init__(self, main_frame, position):
        self.is_set = False
        self.ID = position - 1
        self.hosted_ad_index = 0xFF
        self.default_dict = {}
        #------Geometry below
        subframe_column = (position+1)%2
        subframe_row = int((position-1)/2)
        
        self.subframe = ttk.Frame(main_frame, padding=(10,10,10,10))
        self.subframe.grid(column = subframe_column, row = subframe_row)
        self.subframe.columnconfigure(0, weight = 1)
        for i in range(6):
            self.subframe.rowconfigure(i, weight = 1)
        #-----Widgets below
        self.default_icon = ImageTk.PhotoImage(Image.new("RGB", (32, 32),
                                                          (255, 0, 0)))
        self.icon = ttk.Label(self.subframe, anchor="center")
        self.icon.grid(column = 0, row = 0, sticky=(N, W, E, S))
        self.default_dict[self.icon] = self.default_icon
        
        self.game_name_default_text = "Game name here"
        self.game_name = ttk.Label(self.subframe, anchor="center")
        self.game_name.grid(column = 0,row = 1, sticky=(N, W, E, S))
        self.default_dict[self.game_name] = self.game_name_default_text
        
        
        self.host_name_default_text = "Host name here"
        self.host_name = ttk.Label(self.subframe, anchor="center")
        self.host_name.grid(column = 0,row = 2, sticky=(N, W, E, S))
        self.default_dict[self.host_name] = self.host_name_default_text
        
        self.player_count_default_text = "Player count here"
        self.player_count = ttk.Label(self.subframe, anchor="center")
        self.player_count.grid(column = 0,row = 3, sticky=(N, W, E, S))
        self.default_dict[self.player_count] = self.player_count_default_text
        
        self.seqnum_default_text = "Seq num here"
        self.seqnum = ttk.Label(self.subframe, anchor="center")
        self.seqnum.grid(column = 0,row = 4, sticky=(N, W, E, S))
        self.default_dict[self.seqnum] = self.seqnum_default_text
        
        self.game_desc_default_text = "Game desc here"
        self.game_desc = ttk.Label(self.subframe, anchor="center")
        self.game_desc.grid(column = 0,row = 5, sticky=(N, W, E, S))
        self.default_dict[self.game_desc] = self.game_desc_default_text
        default_entries_loader(self)
    def is_set(self):
        if self.is_set is True:
            return True
        else:
            return False
    
def reset(self):
    if self.is_set is True:
        self.is_set = False
        self.hosted_ad_index = 0xFF
        default_entries_loader(self)
    else:
        return

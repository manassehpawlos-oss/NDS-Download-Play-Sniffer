from tkinter import *
from tkinter import ttk

from options_window.options_fetcher import *

def options_list_to_dict(options_dict):
    returned_list = []
    for phy,item in options_dict.items():
        #returned_list.append(f'{phy}: {item}')
        returned_list.append(f'{phy}: {item}')
    return returned_list

class Options_window:

    def __init__(self, root, top_mainframe):
        self.root = root
        
        mainframe = ttk.Frame(top_mainframe, padding=(3, 3, 12, 12))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe = mainframe
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        #mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(1, weight=1)
        
        self.options_dict = find_wlan_devs()
        self.combobox_default_text = "Select a wlan dev"
        self.selected_device = StringVar(value=self.combobox_default_text)
        self.device_options = ttk.Combobox(mainframe,state = "readonly",
                                           values=options_list_to_dict(find_wlan_devs()),
                                           textvariable=self.selected_device)
        
        self.device_options.bind('<<ComboboxSelected>>', self.selection_clear)
        self.device_options.grid(column=0,row=0)
        
        
        self.killwifi_state = BooleanVar(value=False)
        
        self.killwifi = ttk.Checkbutton(mainframe,text="Disable network manager?",
                                           variable=self.killwifi_state,
                                           onvalue=True,offvalue=False) #checked by default
        self.killwifi.grid(column=0,row=1)
        
        self.start_button = ttk.Button(mainframe, text="Move to scan window")
        self.start_button.grid(column=0, row=2)
        
        self.root.minsize(500,200)
        
    def selection_clear(self,*args):
        self.device_options.selection_clear()
    def selection_check(self,*args):
        return (self.selected_device.get() != self.combobox_default_text)
    def selection_rejected(self,*args):
        print("Not valid")
    def selection_accepted(self,*args):
        print(f'Network turn off: {self.killwifi_state.get()}')
        self.mainframe.grid_remove()
        return self.selected_device.get()
       

# root = Tk()
# Options_Window(root)
# root.mainloop()

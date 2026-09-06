#class file
from binascii import crc32
from scapy.all import *
from PIL import Image

from ads.frame_fcts import *
from ads.adv_fcts import *
#rename fragment_dictionary to fragment_dict

def generate_ad_list(number):
    ad_list = []
    for i in range(number):
        ad_list.append(Advertisement(i))
    return ad_list

def initialize(ad):
    ad.is_assembled = False
    ad.queued_for_display = False
    ad.queued_for_update = False
    ad.occupied_channel = 0 #placeholder
    ad.index_dict = {}
    ad.fragment_dictionary = {}
    ad.bytestream = 0
    ad.name_length = 0
    ad.seqnum = 0
    ad.addr = 0 #convert to int at some point to speed this up
    ad.current_players = 0
    ad.max_players = 0
    ad.player_count = 0
    ad.host_name = "N/A"
    ad.game_name = "N/A"
    ad.game_desc = "N/A"
    ad.palette_raw: list = []
    ad.palette_dictionary = {}
    ad.palette_RGBA: list = []
    ad.tiles: list = []
    ad.image = 0 
class Advertisement():
    """The assembled frame and it's palette/tile data"""
    def __init__(self, ID: int):
        self.ID = ID
        initialize(self)
        
    def reset_ad(self):
        initialize(self)
        
    def ID_display(self):
        print(f"[Object {self.ID}]", end = ": ")
        
    def instance_generator(self,bytestream): #rename
        self.is_assembled = True
        self.queued_for_display = True
        self.name_length = bytestream[0x221]
        self.max_players = bytestream[0x236] #aug 9 - gives correct #.
        self.player_count = f'{self.current_players}/{self.max_players}' #hack fix to get player count to display properly. When all frames update this number, there won't be any problems
        self.host_name = little_to_big_endian(bytestream[0x222:0x222+self.name_length*2],2).decode("utf-16be")
        self.game_name = little_to_big_endian(trailing_00_remover(bytestream[0x238:0x238+96]),2).decode("utf-16be")
        self.game_desc = little_to_big_endian(trailing_00_remover(bytestream[0x298:0x298+192]),2).decode("utf-16be")
        self.palette_raw: list = payload_palette_extractor(bytestream)
        self.palette_dictionary = RGB_LE2byte_to_int(self.palette_raw)
        self.palette_RGBA: list = RGB555_dict_to_RGBA_list(self.palette_dictionary)
        self.tiles: list = payload_tile_extractor(bytestream)
        self.image = game_icon_generator(self.tiles,self.palette_RGBA)
    def first_frag_logger(self,packet,packet_raw,start_of_data):
        beacon_index_dict_assembler(self.index_dict, packet_raw, start_of_data)
        self.addr = packet_raw[self.index_dict["addr"]:self.index_dict["addr"]+6]
        self.occupied_channel = int((packet.ChannelFrequency-2407)/5)
        print(f"Troubleshooting ------------------------------- channel is {self.occupied_channel}")
        current_frag_length = int(packet_raw[self.index_dict["size"]]+0x100*packet_raw[self.index_dict["size"]+1])
        fragment_collector(packet_raw, self.index_dict, self.fragment_dictionary,current_frag_length,self.ID)
    def subsequent_frag_logger(self,packet_raw,start_of_data):
        
        current_frag_length = int(packet_raw[self.index_dict["size"]] + 256*packet_raw[self.index_dict["size"]+1])
        fragment_collector(packet_raw, self.index_dict, self.fragment_dictionary,current_frag_length,self.ID)
        
    def frame_processor_and_claimer(self, packet, packet_raw, start_of_data):
        self.ID_display()
        if not self.fragment_dictionary: #if no frags collected yet
            self.first_frag_logger(packet,packet_raw, start_of_data)
            print("Claimed as first fragment")
            return True #frame belongs to this guy!
        else:
            if self.has_matching_addr(packet_raw) is True: #if this is not first frame and addr is correct
                self.update_seqnum_and_player_count(packet_raw)
                if self.is_assembled:
                    print("Claimed, advert already assembled")
                    self.queued_for_update = True
                    return True
                else: #we take frame
                    self.subsequent_frag_logger(packet_raw, start_of_data)
                    print("Logging frame", end = ", ")
                    if self.is_full(packet_raw) is True:
                        print("Final frame. Assembling now", end = ", ")
                        self.bytestream = entire_payload_assembler(self.fragment_dictionary)
                        self.instance_generator(self.bytestream)
                        return True
                    else:
                        print("Need more frames.")
                        return True
            else:
                print("Packet rejected", end =". ")
                return False
    def is_full(self,packet_raw):
        if self.fragment_dictionary["count"] == len(self.fragment_dictionary)-1:
            return True
        else:
            return False
    def has_matching_addr(self,packet):
        packet_addr = packet[self.index_dict["addr"]:self.index_dict["addr"]+6]
        if packet_addr == self.addr:
            return True
        else:
            return False
        
    def update_seqnum_and_player_count(self,packet_raw): #known to give seqnum bugs
        lower_byte = packet_raw[self.index_dict["seqnum"]]
        lower_byte_calced = int(lower_byte/8) #+(lower_byte%8)*(16*16*16*16), ignored since its so... big. 
        upper_byte = packet_raw[self.index_dict["seqnum"] + 1]
        upper_byte_calced = int(upper_byte/8)*16*16+(upper_byte%8)*16
        
        self.seqnum = lower_byte_calced + upper_byte_calced
        self.current_players=int(packet_raw[self.index_dict["player_count"]])+1
        self.player_count = f'{self.current_players}/{self.max_players}'
    
    def summary(self):
        print("\n\n\n" + self.host_name)
        print(self.game_name)
        print(self.game_desc)
        print(f'{self.current_players}/{self.max_players}', end = "\n\n\n")
    
    def view(self):
        if self.is_assembled:
            self.image.show()
        else:
            print("Can't let you do that, Start Fox.")    
    
    #below are for troubleshooting only
    
    def palette_list_report(self):
        for thing in self.palette_raw:
            hexdump(thing)
        print(f"Palettes has length of {str(len(self.palette_raw))}", end = "\n\n")
    def tiles_list_report(self): 
        console_palette_printer(self.tiles)
        print("\nTiles has length of " + str(len(self.tiles)))
        print(self.tiles)

    def hexdump(self):
        hexdump(self.bytestream)

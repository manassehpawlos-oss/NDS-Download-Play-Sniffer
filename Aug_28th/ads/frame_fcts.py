#fct file
from binascii import crc32
from scapy.all import *
from PIL import Image
import timeit

pcap_filename = "MKDS_and_brainage_2"

def is_beacon(packet):
    if packet.haslayer(Dot11): #802.11 frame
        if packet.type == 0 and packet.subtype == 8: #if beacon
            return True
        else:
            pass
            #print("Non-beacon frame")
    #print("Non-802.11 frame captured. Should not be possible.")
    
def has_proper_CRC(packet: bytes):
    CRC_recieved = packet[-4:]
    CRC_calculated = crc32(packet[:-4]).to_bytes(4,byteorder='little')
    return CRC_calculated == CRC_recieved

def beacon_index_dict_assembler(dictionary, packet: bytes, index_NDS_start: int):
    beacon_index_frame_current = index_NDS_start + int(0x1F)
    beacon_index_frame_final = index_NDS_start + int(0x23)
    beacon_index_payload_start = index_NDS_start + int(0x26)
    beacon_index_payload_size = index_NDS_start + int(0x24)
    beacon_index_frame_current_players = index_NDS_start + 0x1E
    beacon_index_addr_start = 10 #not bytes
    beacon_index_seqnum = 0x16
    
    dictionary["current"] = beacon_index_frame_current
    dictionary["final"] = beacon_index_frame_final
    dictionary["start"] = beacon_index_payload_start
    dictionary["size"] = beacon_index_payload_size
    dictionary["player_count"] = beacon_index_frame_current_players
    dictionary["addr"] = beacon_index_addr_start
    dictionary["seqnum"] = beacon_index_seqnum #lmao will need to account for unique little endian structure
    return True

def fragment_collector(packet: bytes, index_dictionary, fragments_dictionary, length_of_frag,num):
    """Currently contains unreachable conditions, but this is not a bad thing"""
    current_payload_index = int(packet[index_dictionary["current"]])
    extracted_payload = packet[index_dictionary["start"]:index_dictionary["start"] + length_of_frag]
    if "count" not in fragments_dictionary: #first frag, return false
        #print("first frame added")
        fragments_dictionary["count"] = int(packet[index_dictionary["final"]])+1 
        fragments_dictionary[current_payload_index] = extracted_payload
        return
    
    if fragments_dictionary["count"] == len(fragments_dictionary)-1: #dict is full, return
        #print("associated payload already assembled")
        return
    
    if current_payload_index in fragments_dictionary: 
        #print("fragment already logged")
        return
    
    if current_payload_index not in fragments_dictionary: #dict not full. Continue
        #print("adding payload fragment", end = ", ")
        fragments_dictionary[current_payload_index] = extracted_payload
        if fragments_dictionary["count"] == len(fragments_dictionary)-1: 
            #print("final frame added - assembling payload now", end = "\n\n")
            return
        else:
            #print("need more frags")
            return
        
    if fragments_dictionary[current_payload_index] == extracted_payload: #frame is already present, false
        #print("recieved frame is already logged")
        return
            


def frame_info_printer(packet,start_of_data):
    frame_current = packet[start_of_data + int(0x1F)]
    frame_final = packet[start_of_data + int(0x23)]
    mac_addr = packet[13:16]
    print(f"Beacon {frame_current} of {frame_final} from address {bytes(mac_addr).hex()}", end = ", ")

def entire_payload_assembler(payload_dictionary: dict):
    assembled_payload = bytearray()
    for i in range(payload_dictionary["count"]): 
        if i in payload_dictionary:
            print("count is " + str(i), end = ", ")
            assembled_payload += payload_dictionary[i]
            print("length of assembled is " + str(len(assembled_payload)))
        if i not in payload_dictionary:
            print("Damn, we're missing this one: " + str(i))
    return assembled_payload


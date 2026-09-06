#class fct file
from binascii import crc32
from scapy.all import *
from PIL import Image

def payload_palette_extractor(bytestream):
    returned_palette_list = []
    for i in range(16):
        returned_palette_list.append(bytestream[2*i:2*i+2])
    return returned_palette_list

def payload_tile_extractor(bytestream):
    returned_tile_list = []
    start_of_tile_data = 32
    for i in range(start_of_tile_data, start_of_tile_data + 512):
        upper = int(bytestream[i]/16)
        lower = bytestream[i]%16
        returned_tile_list.append(lower)
        returned_tile_list.append(upper)
    return returned_tile_list

def console_palette_printer(tiles):
    for i in range(0,len(tiles),8):
        print("\nTiles sequence " + f'{int(i/8)}', end = ", ")
        for j in range(i,i+8):
            print(str(tiles[j]), end = " ")
    #Note - 8x8 starts from left to right, then top to down. Each 8x8 is drawn by rows from top to bottom. 

def RGB_LE2byte_to_int(pallete_list):
    """Given a 16-len list of 2 bytes each, little endian. Return a dictionary with RGB values for each byte"""
    returned_dictionary = {}
    for i in range(len(pallete_list)):
        int_sum = pallete_list[i][0]+pallete_list[i][1]*256#might be some silly small endian stuff. Check out later. Either need to change math, or change dict.
        blue_555 = int_sum%32
        carryover = int(int_sum/32)
        green_555 = carryover%32
        red_555 = int(carryover/32)
        
        dictionary_to_insert=[blue_555*8, green_555*8, red_555*8] #seems like the colors are little endian.
        returned_dictionary[i] = dictionary_to_insert
    return returned_dictionary

def RGB555_dict_to_RGBA_list(palette_dictionary):
    """Assumes that all NDS frames input data for unused palette entries."""
    returned_list = []
    palette_length= len(palette_dictionary)
    
    for i in range(4):
        returned_list.append(0)
    
    for i in range(1,palette_length):
        temp_list = palette_dictionary[i]
        for RGB_entry in temp_list:
            returned_list.append(RGB_entry)
        returned_list.append(255)
    return returned_list

def game_icon_generator(tiles,palette):
    returned = Image.new('P',(32,32))
    returned.putpalette(palette,'RGBA')
    for i in range(4):
        for j in range(4):
            for k in range(8):
                for l in range(8):
                    current_position = [l+j*8,k+i*8]
                    current_palette = tiles[l+k*8+j*64+i*64*4]
                    returned.putpixel(current_position,current_palette)
    return returned
def trailing_00_remover(bytestream):
    to_return = bytestream
    index = to_return.find(b'\00\00\00')
    if index != -1:
        if index%2 == 0:
            to_return = to_return[:index]
        else:
            to_return = to_return[:index+1]
    return to_return

def little_to_big_endian(bytestream,interval):
    returned_bytes = bytestream
    for i in range(0,len(bytestream),interval):
        bytestream_temp = returned_bytes[i:i+interval]
        bytestream_reversed = bytestream_temp[::-1]
        for j in range(interval):
            returned_bytes[i+j] = bytestream_reversed[j]
    return returned_bytes
from scapy.all import *
from PIL import Image, ImageTk
import timeit
from tkinter import *
from tkinter import ttk
import subprocess


def check_for_new_ad(ad_list):
    returned_list = []
    for ad in ad_list:
        if ad.queued_for_display is True:
            returned_list.append(ad.ID)
    return returned_list

def check_for_updated_ad(ad_list):
    returned_list = []
    for ad in ad_list:
        if ad.queued_for_update is True:
            returned_list.append(ad.ID)
    return returned_list


def check_for_empty_disp(display_list):
    for disp in display_list:
        if disp.is_set is False:
            return disp.ID
    print("script thinks all displays are full")

def check_for_matching_disp(ad_ID, display_list):
    for disp in display_list:
        if disp.hosted_ad_index == ad_ID:
            return disp.ID
    print("check_for_matching_id called incorrectly")
    
def display_new_ad(display, advert):
    advert.queued_for_display = False
    display.is_set = True
    advert.palette_list_report()
    
    display.hosted_ad_index = advert.ID
    display.image = ImageTk.PhotoImage(advert.image)
    display.icon['image'] = display.image
    display.game_name['text'] = advert.game_name
    display.host_name['text'] = advert.host_name
    display.game_desc['text'] = advert.game_desc
    display.player_count['text'] = advert.player_count
    display.seqnum['text'] = advert.seqnum 

def display_updated_ad(display, advert):
    advert.queued_for_update = False
    display.player_count['text'] = advert.player_count
    display.seqnum['text'] = advert.seqnum
    print(f'Advert {advert.ID} updated with display {display.ID}')

def display_ads(ad_list,disp_list):
    IDs_of_new_ads = check_for_new_ad(ad_list)
    if len(IDs_of_new_ads) > 0:
        for ad_ID in IDs_of_new_ads:
            ID_of_empty_disp = check_for_empty_disp(disp_list)
            display_new_ad(disp_list[ID_of_empty_disp], ad_list[ad_ID])

def update_ads(ad_list,disp_list):
    
    IDs_of_updated_ads = check_for_updated_ad(ad_list)
    if len(IDs_of_updated_ads) > 0:
        for ad_ID in IDs_of_updated_ads:
            ID_of_matching_disp = check_for_matching_disp(ad_ID, disp_list)
            #print(f'Troubleshooting - Updated ad recognized - {ad_ID}')
            display_updated_ad(disp_list[ID_of_matching_disp], ad_list[ad_ID])
            #print(f'Troubleshooting - matching slot identified - {ad_ID}')

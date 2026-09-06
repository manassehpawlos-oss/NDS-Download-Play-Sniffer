# NDS-Download-Play-Sniffer

A simple Python program to detect, assemble and display nearby DS Download Play opportunities. 
Uses Pillow 12.3.0 or later, and Scapy 2.7. Runs on Linux, tested with Ubuntu / Mint.

To run the program, download the repository and run `sudo python3 /path/to/files/main.py`. Sudo is needed for sniffing and configuring your wifi card.

The Linux kernel is very picky about allowing access to Channel 13 for 802.11b - if you live in North America, you'll probably need to patch your kernel. Feel free to send an email to manassehpawlos@gmail.com if you're having trouble with that.

On startup, the program will attempt to detect all relevant wifi adapters and configure the one you selected for sniffing. Some wifi cards aren't capable of entering monitor mode for sniffing all nearby wifi frames - try running `sudo check kill` and `sudo airmon-ng [your wifi card]` and run your card on Wireshark to see if captures actually work.

Credits to Micheal Noland for publicizing how the Download Play protocol works, The Wayback Machine for saving the aforementioned info, and [this forum post](https://retrocomputing.stackexchange.com/questions/28071/how-can-i-communicate-with-a-nintendo-ds-using-the-download-play-protocol) for giving me a starting point.

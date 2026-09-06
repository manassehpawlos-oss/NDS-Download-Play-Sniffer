#!/bin/bash
#This script initializes to channel 13, then checks if channel 13 was actually
#set.
if [[ $EUID -ne 0 ]]; then
	echo "This program requires user privileges."
	exit 99
fi

if !(sudo airmon-ng | grep -q $1); then
	echo "Wifi device not found."
	exit 1
fi

if !(sudo airmon-ng start $1 13 > /dev/null); then
	echo "Unable to start wifi device on channel 13"
	exit 2
	#assumes that failing to init to 13 doesn't return a failure.
fi


echo "Started the wifi card"
exit 0

#!/bin/bash

if !(sudo ip link set $1 up); then
	echo "Failed to set $1 up."
	exit 49
fi

if !(sudo iw dev $1 set channel 13); then
	echo "Channel 13 not available for sniffing. Please exit program."
	exit 50
fi

if !(iw dev $1 info | grep "channel 13"); then
	echo "Channel 13 not available for sniffing. Please exit program."
	exit 51
fi



echo "Initialization done!"
exit 0


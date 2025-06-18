#!/bin/bash

#########################################
# This script sets up a dummy ethernet device.
# A K3S setup can use this dummy device to route all
# traffic within a node.  The benefit of this approach
# is two fold:
# 1. If Internet service disappears, components hosted
#locally will not fail and can communicate among each other.
# 2. If a new service provider arises, the components
# will switch over seamlessly to the new Gateway.
#
# Created by Christoper Stewart
# July 2024
############################################

#############################################
# Usage: setupOfflineMode [init or reset]
# Note: this script assumes device icl43 is available,
# IP address 192.168.43.231/24 is available for use and
# is not need for external routing.
############################################

parm=$1

if [ "$parm" == "init" ];
then
    if [ -e /home/icicle/icicleEdge/.localnetworkInstall ]
    then
	echo Local Network Already Installed
    else
	sudo modprobe dummy
	sudo ip link del icl43
	sudo ip link add icl43 type dummy
	sudo ifconfig icl432 hw ether C8:D7:4A:4E:47:60
	sudo ip addr add 192.168.43.231/24 brd + dev icl43 label icl43:0
	sudo ip link set dev icl43 up
	sudo ip route add default via 192.168.43.0 dev icl43 metric 8000000
	
	echo Offline Mode Setup Successfully
	
	cat icl43 > /home/icicle/icicleEdge/.localnetworkInstall
	
    fi
elif [ "$parm" == "reset" ];
then
    rm /home/icicle/icicleEdge/.localnetworkInstall
    sudo ip route del default via 192.168.43.0 dev icl43 metric 8000000
    sudo ip link del icl43
else
    echo Usage: setupOfflineMode [init or reset]
    echo Note script assumptions below:
    echo IP address 192.168.43.231/24 is available for use and
    echo is not need for external routing.
fi

sleep 10

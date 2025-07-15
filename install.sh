#!/bin/bash

################################################################################################
# This script installs OpenPASS and required open-source software on an edge device (laptop).  
# 
# It installs from the stage git repository by default. The packages pulled will be read only.
# If the first parameter is set.  We will shift to the devel repo, allowing write access.
################################################################################################

######################################################################
#                                                                    #
#    ######   #####   ######  ##   ##  #####    ####    ####  ####   #
#   ##    ## ##   ##  ##      ###  ##  ##  ##  ##  ##  ##     ##     #
#   ##    ## ##   ##  ##      #### ##  ##  ##  ##  ##  ##     ##     #
#   ##    ## #######  ######  ## ####  #####   ######   ####   ###   #
#   ##    ## ##       ##      ##  ###  ##      ##  ##      ##    ##  #
#   ##    ## ##       ##      ##   ##  ##      ##  ##      ##    ##  #
#    ######  ##       ######  ##   ##  ##      ##  ##   ####  ####   #
#                                                                    #
######################################################################

# For transparency list every command executed
set -x

# # Check that user has root access via passwordless sudo
WHOAMIROOT="root"
if [ "$WHOAMIROOT" == "`sudo whoami`" ]; then
	echo "Server user is $WHOAMIROOT"
else
	echo "Error: sudo must provide passwordless access to root on the device "
	exit 1
fi

# #Check that current user is icicle
if [ -d "/home/icicle" ]; then
	echo "the directo ry /home/icicle exists"
else
	echo "Error: the directory /home/icicle must exist. Is the user 'icicle' on this device"
	exit 1
fi

WHOAMI="icicle"
if [ "$WHOAMI" == "`whoami`" ]; then
	echo "Current user is $WHOAMI"
else
	echo "Error: the current user should be icicle "
	exit 1
fi


# #If icicleEdge already exists, remove it
if [ -d "/home/icicle/icicleEdge" ]; then
	rm -rf /home/icicle/icicleEdge
else
	echo "This appears to be a fresh install"
fi

#First, we will configure Ubuntu to avoid Hibernate and screenlock
# These features can interfere with the operation of K3S
sudo systemctl mask sleep.target
sudo systemctl mask hibernate.target
sudo systemctl mask hybrid-sleep.target
gsettings set org.gnome.desktop.session idle-delay 0
gsettings set org.gnome.desktop.screensaver lock-enabled false

cd /home/icicle
mkdir icicleEdge
cd icicleEdge
sudo apt-get -y install docker 
sudo apt-get -y install python3 
sudo apt-get -y install git 
sudo apt-get -y install docker wget net-tools curl 
sudo apt-get -y install python3-pip libmariadb3 libmariadb-dev 
sudo apt-get -y install libsdl2-2.0-0

# We must enable (old school) resolv.conf for DNS resolution
sudo systemctl disable --now systemd-resolved.service 
echo nameserver 8.8.4.4 > ./resolv.conf  
if [ -e "/etc/resolv.conf.original" ]; then
	echo "The original resolv.conf has already been saved"
else
	sudo mv /etc/resolv.conf /etc/resolv.conf.original 
fi 
sudo mv ./resolv.conf /etc/resolv.conf  

# Install helm and snap and set up Git
sudo snap install helm --classic
git config --global user.name "ICICLE Edge Admin" 

git config --global user.email "icicle.edge.admin" 

git config --global init.defaultBranch "master" 

# Copy files to correct places
git clone https://github.com/ICICLE-ai/Harmona.git
mkdir bin
mkdir ea1openpass
mkdir helmbase
cp --recursive Harmona/scripts/deployment/* ./bin/
cp --recursive Harmona/scripts/setup/* ./ea1openpass/ 
cp --recursive Harmona/helm-config/*  ./helmbase/ 
echo 'alias kubecmd="sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml"' >> ~/.bashrc 

# Now setup ASU
cd /home/icicle/icicleEdge
sudo echo "devel" > ctxt
chmod +x ctxt
sudo modprobe dummy
sudo ip link del icl231
sudo ip link add icl231 type dummy
sudo ifconfig icl231 hw ether C8:D7:4A:4E:47:50
sudo ip addr add 192.168.231.231/24 brd + dev icl231 label icl231:0
sudo ip link set dev icl231 up
echo Dummy IP: 192.168.231.231
sleep 15

pip3 install softwarepilot
pip3 install pysdl2
pip3 install fastapi
pip3 install py-lz4framed
sudo apt-get -y install python3-softwarepilot



#!/bin/bash
if [ "$1" = "--force" ]; then
    echo "Forcing execution.  Likely bootup run"
else
    if ! [ -f /var/iciclev2/deploy.booted ]; then
	exit 0
    fi
    
    if ! [ -f /var/iciclev2/already.booted ]; then
	echo 1 > /var/iciclev2/already.booted
	exit 1
    fi
fi


if ! [ -f /etc/resolv.kube ]; then
    sed 's/nameserver/nameserver 8.8.8.8\nnameserver/g' /etc/resolv.conf > /etc/resolv.conf.icicle
    cat /etc/resolv.conf.icicle | grep nameserver | tail -n 1 | awk '{print $2}' > /etc/resolv.kube
    cat /etc/resolv.conf.icicle > /etc/resolv.conf
fi
#apt-get update

chmod 777 /var/iciclev2/*
echo devel > /root/environment

#mkdir /root/aptget
#mv /root/base /root/aptget

#echo "deb [trusted=yes] file:/root/aptget/base ./" > /etc/apt/new.sources.list
#cat /etc/apt/sources.list >> /etc/apt/new.sources.list
#mv /etc/apt/new.sources.list /etc/apt/sources.list
#apt-get -y update

#Call the core scripts first
/var/iciclev2/jayzgotdakeys.sh
#/var/iciclev2/softwareenv.sh
/var/iciclev2/code.sh
/var/iciclev2/data.sh


#Add commands to move/organize the Docker container here
echo "1" > /var/iciclev2/deploy.booted
true

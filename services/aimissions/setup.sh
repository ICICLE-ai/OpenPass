#!/bin/bash

sed 's/nameserver/nameserver 8.8.8.8\nnameserver/g' /etc/resolv.conf > /etc/resolv.conf.icicle
cat /etc/resolv.conf.icicle | grep nameserver | tail -n 1 | awk '{print $2}' > /etc/resolv.kube
cat /etc/resolv.conf.icicle > /etc/resolv.conf
# apt-get update

#Call the core scripts first
/var/icicle/jayzgotdakeys.sh
/var/icicle/softwareenv.sh
/var/icicle/code.sh
/var/icicle/data.sh


#Add commands to move/organize the Docker container here
true

#!/bin/bash

apt-get -y install python3 git pip
apt-get -y install curl
apt-get -y install python3-pip 
#apt-get -y install zlib1g-dev libglfw3-dev libsdl2-dev cmake qtbase5-dev build-essential

python3 -m pip install --upgrade pip
apt-get -y install python3-urllib3 python3-dnspython
apt-get -y install python3-django==3.2 python3-flask python3-requests python3-softwarepilot


true

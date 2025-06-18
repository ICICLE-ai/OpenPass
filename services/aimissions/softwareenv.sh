#!/bin/bash

apt-get -y install python3 git pip
pip3 install urllib3 dnspython

pip install --break-system-packages ultralytics
apt-get -y install --upgrade python3-flask
apt-get -y install --upgrade python3-waitress

cd /opt/bitnami/apache/cgi-bin
nohup python3 ModelFlask.py > flask_output.log 2>&1 & disown

true

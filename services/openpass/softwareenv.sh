#!/bin/bash

apt-get -y install --upgrade python3 git pip 
#additional packages for cropModelService
apt-get -y install --upgrade wget
#apt-get -y python3-opencv
apt-get -y install --upgrade python3-dnspython
apt-get -y install sshpass

#additional packages for cropModelService
apt-get -y install --upgrade python3-tensorflow-cpu
apt-get -y install --upgrade python3-urllib3
apt-get -y install --upgrade python3-jsonify
apt-get -y install --upgrade python3-flask

# additional packages for flightpath planner
apt-get -y install --upgrade python3-matplotlib
apt-get -y install --upgrade python3-seaborn
apt-get -y install --upgrade python3-datetime
apt-get -y install --upgrade python3-scipy

# KAI (9/25/24): Adding GPS mission essential libraries 
apt-get -y install --upgrade python3-geopy
apt-get -y install --upgrade python3-folium

# additional packages for rededge
#apt-get -y install curl 
#wget https://go.dev/dl/go1.20.5.linux-amd64.tar.gz
#rm -rf /usr/local/go
#tar -C /usr/local -xzf go1.20.5.linux-amd64.tar.gz



# additional packages for flightpath planner
#pip3 install matplotlib seaborn datetime scipy

# additional packages for Yolov5
# Chris' note to Kevyn (9/03/24) 
# --- The commented section below should be move to pytorch ms
# --- and after moving you shoud 
# --- consider using apt-get -y install python3-(package_name)
# --- instead oof the venv environment.  The latter is a blank
# --- slate and will require re-downloading dependencies already
# --- on the image.  

#apt -y install python3-venv
#python3 -m venv venv
#source venv/bin/activate
#pip install markupsafe
#pip install Flask
#pip install torch
#pip install opencv-python
#pip install pandas
#pip install waitress
#pip install requests
#pip install Pillow

true

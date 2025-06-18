#!/bin/bash

git config --global user.name "devel"
git config --global user.email "devel"
git config --global core.sshcommand "ssh -i /root/dabDeveloperRSA"
git config --global init.defaultBranch "master"

rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED

#Add commands to download code here
cd /root
# Make the the cgi-bin directoy for executing python scripts
mkdir /opt/bitnami/apache/cgi-bin/
mkdir /opt/bitnami/apache2/htdocs/userfiles/
mkdir /opt/bitnami/apache2/htdocs/mscopy/

# Get a copy of the website code
sleep
git clone devel@149.165.169.119:/volume/devel/openpasswebsite.git /root/openpasswebsite
cp -r /root/openpasswebsite/cgi-bin/* /opt/bitnami/apache/cgi-bin/
cp -r /root/openpasswebsite/js /opt/bitnami/apache2/htdocs/
cp -r /root/openpasswebsite/css /opt/bitnami/apache2/htdocs/
cp -r /root/openpasswebsite/*html /opt/bitnami/apache2/htdocs/
cp -r /root/openpasswebsite/*json /opt/bitnami/apache2/htdocs/
#mkdir /root/go
#cd /root/go
#git clone https://github.com/reddec/trusted-cgi.git
#cd /root

#cp -r /root/openpasswebsite/go/028bec31-2c50-4cd5-b0b3-e4832c4fc541/ /root/go/trusted-cgi
#cp -r /root/openpasswebsite/go/ICICLE_TEMPLATE /root/go/trusted-cgi
#cp -r /root/openpasswebsite/go/pkg /root/go/

#Start trusted-cgi
#cd /root/go/trusted-cgi
#export PATH=$PATH:/usr/local/go/bin
#export GOPATH=/root/go
#git lfs install
#git lfs pull
#GOPATH=/root/go /usr/local/go/bin/go run cmd/trusted-cgi/main.go & < /dev/null
#cr /root

# Get a copy of the rededge middleware
# Deprecated
#git clone devel@149.165.169.119:/volume/devel/rededge.git /root/rededge
#cp /root/rededge/implementations/rededgecall.local.py /root/rededge/rededgecall.py
#cp /root/rededge/implementations/rededgeFlask.py /root/rededge/rededgeFlask.py
#chmod 777 /root/rededge/*py
#python3 /root/rededge/rededgeinstall.py



# Get a copy of the waypoint tool
#git clone https://github.com/jcjumley/FlightPathBuilder.git /root/FlightPathBuilder


# Get a copy of the base Microservices Services Codes
# The copy the code to cgi-bin
git clone devel@149.165.169.119:/volume/devel/baseMSservices.git /root/mscode
mv /root/mscode/*py /opt/bitnami/apache/cgi-bin/


# Make the scripts in cgi-bin executable
chmod 777 /opt/bitnami/apache/cgi-bin/*
chmod 777 /opt/bitnami/apache/htdocs
chmod 777 /opt/bitnami/apache/htdocs/*
chmod 777 /opt/bitnami/apache/htdocs/userfiles
chmod 777 /opt/bitnami/apache2/htdocs/mscopy

#Move the correct Flight_Path_Builder.py into place
#cp /root/openpasswebsite/Build_Flight_Paths_with_Boundary.py /root/FlightPathBuilder

true

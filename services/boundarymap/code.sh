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
mkdir /opt/bitnami/apache/htdocs/userfiles/


# Get a copy of the website code
git clone devel@149.165.169.119:/volume/devel/boundarymapcode.git /root/boundarymapcode
cp /root/boundarymapcode/cgi-bin/* /opt/bitnami/apache/cgi-bin/
cp /root/boundarymapcode/public/* /opt/bitnami/apache2/htdocs/

# Get a copy of the waypoint tool
git clone https://github.com/jcjumley/FlightPathBuilder.git /root/FlightPathBuilder



# Get a copy of the base Microservices Services Codes
# The copy the code to cgi-bin
git clone devel@149.165.169.119:/volume/devel/baseMSservices.git /root/mscode
mv /root/mscode/*py /opt/bitnami/apache/cgi-bin/

cd /root/boundarymapcode
npm install
nohup npm start &


# Make the scripts in cgi-bin executable
chmod 755 /opt/bitnami/apache/cgi-bin/*
chmod 777 /opt/bitnami/apache/htdocs/userfiles/
chmod 755 /opt/bitnami/apache/htdocs/
chmod 755 /root
chmod 755 /root/boundarymapcode/
chmod 775 /root/boundarymapcode/*

#Move the correct Flight_Path_Builder.py into place
cp /root/boundarymapcode/Build_Flight_Paths_with_Boundary.py /root/FlightPathBuilder


true

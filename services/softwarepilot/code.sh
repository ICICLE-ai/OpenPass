#!/bin/bash

git config --global user.name "devel"
git config --global user.email "devel"
git config --global core.sshcommand "ssh -i /root/dabDeveloperRSA"
git config --global init.defaultBranch "master"

rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED

#Add commands to download code here

#First configure the /root directory
cd /root
chmod 744 /root/environment

# Make the the cgi-bin directoy for executing python scripts
mkdir /opt/bitnami/apache/cgi-bin/


# Get a copy of the website code
git clone devel@149.165.169.119:/volume/devel/softwarepilotservice.git /root/softwarepilotservice
cp -r /root/softwarepilotservice/cgi-bin/* /opt/bitnami/apache/cgi-bin/
chmod 740 root/softwarepilotservice/private*
cp -r /root/softwarepilotservice/*html /opt/bitnami/apache2/htdocs/
cp -r /root/softwarepilotservice/css /opt/bitnami/apache2/htdocs/
cp -r /root/softwarepilotservice/js /opt/bitnami/apache2/htdocs/

# Get a copy of the base Microservices Services Codes
# The copy the code to cgi-bin
git clone devel@149.165.169.119:/volume/devel/baseMSservices.git /root/mscode
cp -r /root/mscode/*py /opt/bitnami/apache/cgi-bin/

# Make the scripts in cgi-bin executable
chmod 755 /opt/bitnami/apache/cgi-bin/*
chmod 777 /opt/bitnami/apache/htdocs/
chmod 711 /root


true

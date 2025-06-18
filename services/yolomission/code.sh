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
mkdir /opt/bitnami/apache2/htdocs/latest
mkdir /opt/bitnami/apache2/htdocs/latest/photo
mkdir /opt/bitnami/apache2/htdocs/latest/stream
mkdir /opt/bitnami/apache2/htdocs/repo
mkdir /opt/bitnami/apache2/htdocs/repo/photo
mkdir /opt/bitnami/apache2/htdocs/repo/stream

# Get a copy of the website code
git clone devel@149.165.169.119:/volume/devel/yolomissionsrc.git /root/yolomissionsrc
cp -r /root/yolomissionsrc/cgi-bin/* /opt/bitnami/apache/cgi-bin/
cp /root/yolomissionsrc/*html /opt/bitnami/apache2/htdocs/

# Get a copy of the base Microservices Services Codes
# The copy the code to cgi-bin
git clone devel@149.165.169.119:/volume/devel/baseMSservices.git /root/mscode
mv /root/mscode/*py /opt/bitnami/apache/cgi-bin/

# Make the scripts in cgi-bin executable
chmod 777 /opt/bitnami/apache/cgi-bin/*
chmod 777 /opt/bitnami/apache/htdocs
chmod 777 /opt/bitnami/apache/htdocs/latest
chmod 777 /opt/bitnami/apache/htdocs/latest/photo
chmod 777 /opt/bitnami/apache/htdocs/latest/stream
chmod 777 /opt/bitnami/apache/htdocs/repo
chmod 777 /opt/bitnami/apache/htdocs/repo/photo
chmod 777 /opt/bitnami/apache/htdocs/repo/stream

true

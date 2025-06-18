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
git clone devel@149.165.169.119:/volume/devel/icicleDABWeb.git /root/icicleDABWeb
cp -r /root/icicleDABWeb/cgi-bin/* /opt/bitnami/apache/cgi-bin/
chmod 740 root/icicleDABWeb/private*
cp -r /root/icicleDABWeb/*html /opt/bitnami/apache2/htdocs/
cp -r /root/icicleDABWeb/ei /opt/bitnami/apache2/htdocs/
cp -r /root/icicleDABWeb/icicleEdgeConfigureTool.sh /opt/bitnami/apache2/htdocs/
cp -r /root/icicleDABWeb/icicleASUEdgeConfigureTool.sh /opt/bitnami/apache2/htdocs/
cp -r /root/icicleDABWeb/css /opt/bitnami/apache2/htdocs/
cp -r /root/icicleDABWeb/js /opt/bitnami/apache2/htdocs/

# Get a copy of the base Microservices Services Codes
# The copy the code to cgi-bin
git clone devel@149.165.169.119:/volume/devel/baseMSservices.git /root/mscode
cp -r /root/mscode/*py /opt/bitnami/apache/cgi-bin/
mkdir /opt/bitnami/apache/htdocs/mscopy


# Make the scripts in cgi-bin executable
chmod 755 /opt/bitnami/apache/cgi-bin/*
chmod 711 /root


true

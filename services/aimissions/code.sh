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
mkdir /opt/bitnami/apache/cgi-bin/Helper
mkdir /opt/bitnami/apache/cgi-bin/Models
mkdir /opt/bitnami/apache/htdocs/
mkdir /opt/bitnami/apache/htdocs/repo/
mkdir /opt/bitnami/apache/htdocs/result/
mkdir /opt/bitnami/apache/htdocs/zipDir
mkdir /opt/bitnami/apache/htdocs/mscopy/

# Get a copy of the website code
git clone devel@149.165.169.119:/volume/devel/aimissions.git /root/aimissions
cp -r /root/aimissions/cgi-bin/* /opt/bitnami/apache/cgi-bin/
cp -r /root/aimissions/*html /opt/bitnami/apache2/htdocs/

# Get a copy of the base Microservices Services Codes
# The copy the code to cgi-bin
git clone devel@149.165.169.119:/volume/devel/baseMSservices.git /root/mscode
mv /root/mscode/*py /opt/bitnami/apache/cgi-bin/

# Make the scripts in cgi-bin executable
chmod 777 /opt/bitnami/apache/cgi-bin/*
chmod 777 /opt/bitnami/apache/htdocs/repo
chmod 777 /opt/bitnami/apache/htdocs/result
chmod 777 /opt/bitnami/apache/htdocs/zipDir
chmod 777 /opt/bitnami/apache/htdocs/mscopy

true

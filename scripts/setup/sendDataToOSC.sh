#!/bin/bash

echo "Starting with tranfering data...."

echo "Identifying the pods name..."
POD_PREFIX="i54292openpass"
POD_NAME=`sudo kubectl get pods --no-headers | grep "$POD_PREFIX" | awk '{print $1}'`
echo "Pod name identified as: $POD_NAME"

echo "Getting all the asset paths...."
LOCAL_ASSET_PATHS=("/home/icicle/icicleEdge/ea1openpass/assets/" "/home/icicle/icicleEdge/local.softwarepilotservice/static")
POD_ASSET_PATHS=("$POD_NAME:/opt/bitnami/apache/htdocs/userfiles/" "$POD_NAME:/opt/bitnami/apache2/htdocs/userfiles/")

for i in "${LOCAL_ASSET_PATHS[@]}"; do
    echo "Source Detected: $i"
done
for i in "${POD_ASSET_PATHS[@]}"; do
    echo "Source Detected: $i"
done

echo "Starting the upload...."
read -p "Enter your OSC username: " USERNAME
read -s -p "Enter your OSC password: " PASSWORD
echo "Username entered: $USERNAME"
echo "Transferring pod files to local directory...."
for i in "${POD_ASSET_PATHS[@]}"; do
    sudo kubectl cp $i /home/icicle/icicleEdge/ea1openpass/assets/
done
echo "Initiating all files transfer...."
for i in "${LOCAL_ASSET_PATHS[@]}"; do
    sshpass -p $PASSWORD scp -r $i $USERNAME@sftp.osc.edu:/fs/ess/PAS2699/openpass_data/
done
echo "✅🚀Done transfering files to OSC✅🚀"
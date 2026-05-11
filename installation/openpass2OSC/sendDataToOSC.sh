#!/bin/bash

echo "Starting with transferring data...."

echo "Identifying the pods name..."
POD_PREFIX="i54292openpass"
POD_NAME=`sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml get pods --no-headers | grep "$POD_PREFIX" | awk '{print $1}'`
echo "Pod name identified as: $POD_NAME"

echo "Getting all the asset paths...."
LOCAL_ASSET_PATHS=("/home/icicle/icicleEdge/installation/assets/" "/home/icicle/icicleEdge/local.softwarepilotservice/static")
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
mkdir -p /home/icicle/icicleEdge/installation/assets/
for i in "${POD_ASSET_PATHS[@]}"; do
    sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml cp "$i" /home/icicle/icicleEdge/installation/assets/
done
echo "Initiating all files transfer...."
for i in "${LOCAL_ASSET_PATHS[@]}"; do
    sshpass -p "$PASSWORD" scp -r "$i" "$USERNAME"@sftp.osc.edu:/fs/ess/PAS2699/openpass_data/
done
echo "✅🚀Done transfering files to OSC✅🚀"
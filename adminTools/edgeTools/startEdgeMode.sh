#!/bin/bash

bash /home/icicle/icicleEdge/adminTools/edgeTools/setupOfflineMode.sh reset
bash /home/icicle/icicleEdge/adminTools/edgeTools/setupOfflineMode.sh init

sleep 3
echo "Restarting k3s"
sudo systemctl restart k3s



NODE_NAME=`sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml get nodes| tail -n 1 | awk '{print $1}' `
EDGE_ID=$NODE_NAME
EDGE_ID+="-edgedevel"
sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml label node $NODE_NAME icicletype=edgedevel
echo $EDGE_ID > ~/.ssh/icicletype


cd /home/icicle/icicleEdge
./bin/deployEdgeMicroservice.py -home `pwd` -devel -edge edgedevel 30080website
sleep 15
./bin/deployEdgeMicroservice.py -home `pwd` -devel -edge edgedevel 54292openpass
echo Deployed OpenPASS!  Waiting more seconds
sleep 15
./bin/deployEdgeMicroservice.py -home `pwd` -devel -edge edgedevel 43210asu
echo Deployed ASU service!  Waiting more seconds
sleep 15
./bin/deployEdgeMicroservice.py -home `pwd` -devel -edge edgedevel 8383boundarymap
echo Deployed map utilities
sleep 15
./bin/deployEdgeMicroservice.py -home `pwd` -devel -edge edgedevel 2222yolomissions 
echo Deployed Yolo Mission in the background
sleep 15
./bin/deployEdgeMicroservice.py -home `pwd` -devel -edge edgedevel 1212aimissions 
echo Deployed AI Mission in the background

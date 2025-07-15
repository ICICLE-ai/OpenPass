#!/bin/bash

echo "Shutting down local instances to get up-to-date IP address"
echo "Killall and Uninstall k3s"
sudo bash /usr/local/bin/k3s-killall.sh
sudo bash /usr/local/bin/k3s-uninstall.sh
sudo rm /var/lib/rancher/k3s/server/token
sudo rm -rf /etc/ceph \
       /etc/cni \
       /etc/kubernetes \
       /etc/rancher \
       /opt/cni \
       /opt/rke \
       /run/secrets/kubernetes.io \
       /run/calico \
       /run/flannel \
       /var/lib/calico \
       /var/lib/etcd \
       /var/lib/cni \
       /var/lib/kubelet \
       /var/lib/rancher\
       /var/log/containers \
       /var/log/kube-audit \
       /var/log/pods \
       /var/run/calico



sleep 3
bash /home/icicle/icicleEdge/ea1openpass/setupOfflineMode.sh reset
bash /home/icicle/icicleEdge/ea1openpass/setupOfflineMode.sh init

# Do a fresh install
echo "Installing K3s -- sudo curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC=\"server --flannel-iface=icl43\" sh -"
sudo curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --flannel-iface=icl43" /bin/sh -
sleep 5


NODE_NAME=`sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml get nodes| tail -n 1 | awk '{print $1}' `
EDGE_ID=$NODE_NAME
EDGE_ID+="-edgedevel"
sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml label node $NODE_NAME icicletype=edgedevel
echo $EDGE_ID > ~/.ssh/icicletype



cd /home/icicle/icicleEdge
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 30080website
echo Deployed website!  Waiting more seconds
sleep 15
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 54292openpass
echo Deployed OpenPASS!  Waiting more seconds
sleep 15
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 43210asu
echo Deployed ASU service!  Waiting more seconds
sleep 15
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 8383boundarymap
echo Deployed map utilities
sleep 15
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 2222yolomissions 
echo Deployed Yolo Mission in the background
sleep 15
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 1212aimissions 
echo Deployed AI Mission in the background
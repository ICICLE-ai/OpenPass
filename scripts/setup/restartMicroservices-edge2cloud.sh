#!/bin/bash
parm=$1

if [ "$parm" != "skip" ];
then
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
    bash /home/icicle/icicleEdge/adminTools/edgeTools/setupOfflineMode.sh reset
    bash /home/icicle/icicleEdge/adminTools/edgeTools/setupOfflineMode.sh init

    # Launch edge-2-cloud setup
    bash /home/icicle/icicleEdge2Cloud/launchJetstream2Cluster.sh -c 2 -m 180
fi


cd /home/icicle/icicleEdge
./bin/deployMicroservice.py -home `pwd` -devel -edge edge2cloud 30080website
echo Deployed website!  Waiting more seconds
sleep 12
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 54292openpass
echo Deployed OpenPASS!  Waiting more seconds
sleep 12
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 43210asu
echo Deployed ASU service!  Waiting more seconds
sleep 12
#./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 8383boundarymap
#echo Deployed map utilities
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 2222yolomissions 
echo Deployed Yolo Mission in the background
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 1212aimissions 
echo Deployed AI Mission in the background


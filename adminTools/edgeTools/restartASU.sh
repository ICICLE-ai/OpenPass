#!/bin/bash

#sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml label nodes `hostname | tr '[:upper:]' '[:lower:]'` icicletype=edgedevel
cd /home/icicle/icicleEdge
killall -9 icicleasu

set -x
sudo modprobe dummy
sudo ip link del icl231
sudo ip link add icl231 type dummy
sudo ifconfig icl231 hw ether C8:D7:4A:4E:47:50
sudo ip addr add 192.168.231.231/24 brd + dev icl231 label icl231:0
sudo ip link set dev icl231 up
echo Dummy IP: 192.168.231.231

CTXT=`cat /home/icicle/icicleEdge/ctxt`

rm -rf local.softwarepilotservice
sudo pip install py-lz4framed
git clone $CTXT@149.165.169.119:/volume/$CTXT/softwarepilotservice.git local.softwarepilotservice
sed -i 's/from OpenGL import GLX/\#OpenGL import GLX/g' $HOME/.local/lib/python3.10/site-packages/olympe/video/renderer.py
cd local.softwarepilotservice
sudo cp /usr/bin/python3 /usr/bin/icicleasu
nohup /usr/bin/icicleasu /home/icicle/icicleEdge/local.softwarepilotservice/onDevice/main.py >& localservice.logs & disown
mkdir static
cd static
nohup /usr/bin/icicleasu -m http.server --bind 192.168.231.231 2311 >& httpservice.logs & disown
echo Local Service Launched

sleep 5

true


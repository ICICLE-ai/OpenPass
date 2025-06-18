#!/bin/bash
# This script assumes the icicleEdge folder is installed in the home directory
cd ~
cd icicleEdge
set -x
sudo modprobe dummy
sudo ip link del icl231
sudo ip link add icl231 type dummy
sudo ifconfig icl231 hw ether C8:D7:4A:4E:47:50
sudo ip addr add 192.168.231.231/24 brd + dev icl231 label icl231:0
sudo ip link set dev icl231 up
echo Dummy IP: 192.168.231.231

rm -rf local.softwarepilotservice
sudo pip install py-lz4framed
git clone devel@149.165.169.119:/volume/devel/softwarepilotservice.git local.softwarepilotservice
sed -i 's/from OpenGL import GLX/\#OpenGL import GLX/g' $HOME/.local/lib/python3.10/site-packages/olympe/video/renderer.py
cd local.softwarepilotservice
sudo cp /usr/bin/python3 /usr/bin/icicleasu
icicleasu onDevice/main.py >& localservice.logs & disown
mkdir static
cd static
icicleasu -m http.server --bind 192.168.231.231 2311 >& httpservice.logs & disown
echo Local Service Launched



true

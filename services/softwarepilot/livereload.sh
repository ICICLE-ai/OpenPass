#!/bin/bash

fltr=""
args=$#
if [  $args -gt 0 ]; then fltr="$1"; fi

ldir=""
lsrc=""
dest=""

kube_copy() {    
    curd=`pwd`
    cd $ldir

    for long_name in $lsrc;
    do
	echo $fltr
	if [  $args -gt 0 ]; then
	    if [ "$fltr" != "$long_name" ]; then
		continue
	    fi
	fi
	name=$long_name #`echo $long_name | awk -F \/ '{print $2}'`
	echo sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml cp `pwd`/$name `/home/icicle/icicleEdge/bin/getFirstPod.sh i43210asu`:$dest/$name
	sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml cp `pwd`/$name `/home/icicle/icicleEdge/bin/getFirstPod.sh i43210asu`:$dest/$name
	
	echo sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml exec -it `/home/icicle/icicleEdge/bin/getFirstPod.sh i43210asu` -- chmod 777 $dest/$name
	sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml exec -it `/home/icicle/icicleEdge/bin/getFirstPod.sh i43210asu` -- chmod 777 $dest/$name
    done
    cd $curd

}

ldir="drone-contoller/api/"
lsrc="*"
dest="/root/softwarepilotservice/onDevice"
kube_copy

ldir="drone-contoller/core/"
lsrc="*"
dest="/root/softwarepilotservice/onDevice"
kube_copy

ldir="drone-contoller/testing/"
lsrc="*"
dest="/root/softwarepilotservice/onDevice"
kube_copy

ldir="."
lsrc="*sh"
dest="/root/softwarepilotservice/"
kube_copy
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
	echo sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml cp `pwd`/$name `/home/icicle/icicleEdge/bin/getFirstPod.sh i1212aimissions`:$dest/$name
	sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml cp `pwd`/$name `/home/icicle/icicleEdge/bin/getFirstPod.sh i1212aimissions`:$dest/$name
	
	echo sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml exec -it `/home/icicle/icicleEdge/bin/getFirstPod.sh i1212aimissions` -- chmod 777 /opt/bitnami/apache2/$dest/$name
	sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml exec -it `/home/icicle/icicleEdge/bin/getFirstPod.sh i1212aimissions` -- chmod 777 $dest/$name
    done
    cd $curd

}

ldir="cgi-bin/"
lsrc="*py"
dest="/opt/bitnami/apache2/cgi-bin"
kube_copy

ldir="cgi-bin/"
lsrc="*pt"
dest="/opt/bitnami/apache2/cgi-bin"
kube_copy

ldir="cgi-bin/Helper"
lsrc="*py"
dest="/opt/bitnami/apache2/cgi-bin/Helper"
kube_copy

ldir="cgi-bin/Models"
lsrc="*py"
dest="/opt/bitnami/apache2/cgi-bin/Models"
kube_copy

ldir="js/"
lsrc="*"
dest="/opt/bitnami/apache2/htdocs/js"
kube_copy

ldir="css/"
lsrc="*"
dest="/opt/bitnami/apache2/htdocs/css"
kube_copy

ldir="."
lsrc="*html"
dest="/opt/bitnami/apache2/htdocs/"
kube_copy

ldir="."
lsrc="*json"
dest="/opt/bitnami/apache2/htdocs/"
kube_copy

#!/bin/bash

targ_file=$1
msrv_name=$2
full_msid=`sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml get pods | grep $msrv_name | head -n 1 | awk '{print $1}'`
sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml cp $targ_file $full_msid:/root/

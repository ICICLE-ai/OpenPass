#!/bin/bash

sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml get pods
echo Now running NETSTAT conditioned for icicleASU
echo 
netstat -tlnp | grep icicle
sleep 10


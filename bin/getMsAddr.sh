#/bin/bash
sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml get services | grep $1 | awk '{print $3":"$5}' | awk -F / '{print $1}'

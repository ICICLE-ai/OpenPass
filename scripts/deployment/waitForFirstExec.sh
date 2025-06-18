found=0
while [ $found == 0 ]
do
      podname=`sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml get pods | grep $1 | head -n 1 | awk '{print $1}'`
      if [ "$podname" != "" ]
      then
	  found=1
      else
	  sleep 5		
      fi
done
found=0
while [ $found == 0 ]
do
      result=`sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml  exec -it $podname -- echo icicle`

      if [ "$result" != "" ]
      then
	  found=1
      else
	  sleep 5		
      fi
done

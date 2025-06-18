#!/usr/bin/python3
# This script deploys a microservice using Helm on our K3s Kubernetes cluster
#
# Presumptions:
# 1. This script is NOT thread safe.  It is expected to be run by a system admin directly from the console
# 2. Helm charts and ICICLE modifiers are expected to be small (<<1 GB)
# 3. Naming must follow conventions in the Patterns of Development Document on MS Teams
# 4. The script will build the dictionary stored in MariaDB as it progresses along / A failed installation will not update DB
#
# Basic procedure:
# 1. Check that the micorservice name follows correct naming protocol
# 2. Check to see if the port is currently in use... if so this is a redeploy
# 3. Create the /home/ubuntu/scratch directory where we will glue data into appropriate places
# 4. Check out the microservice GIT to /home/ubuntu/scratch/deploy
# 5. Copy the standard Helm apache template (Bitnami) located at /home/ubuntu/helmbase to /home/ubuntu/scratch/helm
# 6. Copy key files from deploy to helm
# 6b. Update ports
# 7. If redeploy (helm uninstall first) 
# 8. Helm install
# 8b. Wait a 2 minutes
# 9. Run unit tests
# 10. Check unit tests output CSV file
# 11. If failure, helm uninstall
# 12. Else, add to database as active service

#written for the ICICLE environment by Christopher Stewart
# Jan 15, 2023                                                                                                                                                                                                                               

import os
import sys
import re
import time

portNum = 0
baseDir = "/home/ubuntu/"
edgePck = "/home/ubuntu/edgePackages"
scratch = "/home/ubuntu/scratch"
msTempD = "/home/ubuntu/scratch/deploy"
msExist = False
helmCre = "/home/ubuntu/scratch/helmbase"
waittme = 15
msProps = ""
develOp = False
msIpAdd = "127.0.0.1"
nameCnt = 0
edgeNme = "world"
edgeDeployment = False
ctxtNme = "stage"


def fileAppendLine(fleName, lineOut):
    f=open(fleName,'a+')
    if (f.writable() == True):
        f.writelines(lineOut)
    f.close()

def fileReadLine(fleName):
    f=open(fleName,'r')
    if (f.readable() == True):
        readOut=f.readline().strip()
    f.close()
    return (readOut)


# Getting the length of command
# line arguments
n = len(sys.argv)
i = 1
while (i < n):
    if sys.argv[i] == "-devel":
        develOp = True
        msIpAdd = "149.165.169.119"
    elif sys.argv[i] == "-edge":
        edgeDeployment = True
        i=i+1
        edgeNme = sys.argv[i]
    elif sys.argv[i] == "-home":
        i=i+1
        baseDir = sys.argv[i]
        edgePck = sys.argv[i]+"/edgePackages"
        scratch = sys.argv[i]+"/scratch"
        msTempD = sys.argv[i]+"/scratch/deploy"
        helmCre = sys.argv[i]+"/scratch/helmbase"
    else: 
        msTitle = sys.argv[i]
        nameCnt = nameCnt+1
    i=i+1
    
if (nameCnt != 1 ):
    print ("Error.  The input line contained " + str(nameCnt) + " microservice names.  There should be exactly 1.  Did you mistype a parameter?")
    sys.exit(1)

    
# 1. Check that the micorservice name follows correct naming protoco
if re.search("^[0-9]+[a-zA-Z0-9]+$",msTitle):
    s = re.split("[a-zA-Z]",msTitle)
    portNum = s[0]
    k3sMsID = "i"+msTitle #k3s names must begin with a-z
    print ("Deploying Microservice on port: "+ msTitle)
else:
    print (msTitle + " is not a valid repo name.  Microservices must begin with a number N and the descriptive name D.  Regular expression is [0-9]+[a-zA-Z0-9]+")
    sys.exit(1)

# While we are here, let's check if this is a website deployment which is special
websiteDeployment = False
if re.search(".*30080website.*$",msTitle):
    websiteDeployment = True


# 1b. Check the context--- that is what ssh key and server name to use
ctxtNme = fileReadLine(baseDir+"/ctxt")


# 2. Check to see if the port is currently in use... if so this is a redeploy

# 3. Create the /home/ubuntu/scratch directory where we will glue data into appropriate place
os.system('rm -rf %s' % scratch)
os.system('mkdir %s' % scratch)
doesExist = os.path.exists(scratch)
if (doesExist == False):
    print ("Error. The home scratch directory could not be created. Set the -home parameter?")
    sys.exit(1)

os.chdir('%s' % scratch)


# 4. Check out the microservice GIT to /home/ubuntu/scratch/deploy
if (develOp == False):
    os.system('bash '+baseDir+'/bin/gitconfig.sh')


print('cp -r /home/icicle/icicleLocalGit/devel/' + msTitle + ' ' + msTempD)
os.system('cp -r /home/icicle/icicleLocalGit/devel/' + msTitle + ' ' + msTempD)
doesExist = os.path.exists(msTempD)
if (doesExist == False):
    print ("Unable to clone the repo.  Does it exist?")    
    sys.exit(1)
    
#4b. Set up the correct development setup.sh
if (develOp == True):
    setupDevl = os.path.exists(msTempD+'/setup.devel.sh')
    if (setupDevl == False):
        print ("WARNING: -devel specified but setup.devel.sh absent")
    else:
        os.system('cp '+msTempD+'/setup.devel.sh '+msTempD+'/setup.sh')
        
# 5. Copy the standard Helm apache template (Bitnami) located at /home/ubuntu/helmbase to /home/ubuntu/scratch/helmbase
# 6. Copy key files from deploy to helm
os.system('cp -r ' + baseDir + '/helmbase ' + scratch)
os.system('cp -r ' + msTempD + '/* ' + helmCre +'/')


# 6b. Update ports and fullname override
print('sed -i \'s/numPort/'+portNum+'/g\' '+ helmCre + '/values.yaml')
os.system('sed -i \'s/numPort/'+portNum+'/g\' '+ helmCre + '/values.yaml')
os.system('sed -i \'s/fullnameOverride:DAB/fullnameOverride: \"'+k3sMsID+'\"/g\' '+ helmCre + '/values.yaml')

#6c. If it is the website (only for the website) we need to set a fixed IP for the load balancer
if websiteDeployment == True:
    print("This is a website deployment.  clusterIP will run 10.43.195.204")
    print('sed -i \'s/clusterIP: \"\"/'+'clusterIP: \"10.43.195.204\"/g\' '+ helmCre + '/values.yaml')
    os.system('sed -i \'s/clusterIP: \"\"/'+'clusterIP: \"10.43.195.204\"/g\' '+ helmCre + '/values.yaml')

#6d. If this is an edge deployment, we must replace icicletype with the edge resource name
if edgeDeployment == True:
    print("This is an edge deployment. Kubernetes should schedule on a nodetype: " + edgeNme)
    print('sed -i \'s/icicletype: world/'+'icicletype: '+edgeNme+'/g\' '+ helmCre + '/values.yaml')
    os.system('sed -i \'s/icicletype: world/'+'icicletype: '+edgeNme+'/g\' '+ helmCre + '/values.yaml')




# 7. If redeploy (helm uninstall first) ---- Actually it doesn't hurt to clear out first, just in case
print('sudo helm --kubeconfig /etc/rancher/k3s/k3s.yaml delete ' + k3sMsID + ' ')
os.system('sudo helm --kubeconfig /etc/rancher/k3s/k3s.yaml delete ' + k3sMsID + ' ' )
print("Waiting" + str(waittme) +" seconds...")
time.sleep(waittme)
    
# 8. Helm install
print('sudo helm --kubeconfig /etc/rancher/k3s/k3s.yaml install ' + k3sMsID + ' ' + helmCre)
os.system('sudo helm --kubeconfig /etc/rancher/k3s/k3s.yaml install ' + k3sMsID + ' ' + helmCre)
os.system("bash "+baseDir+"/bin/waitForFirstPod.sh "+k3sMsID)
os.system("bash "+baseDir+"/bin/waitForFirstExec.sh "+k3sMsID)
#print("Waiting" + str(waittme) +" seconds...")
#time.sleep(waittme)

#8b. Copy MSfolder into deployment
print('sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml  cp '+msTempD+' `'+ baseDir+'/bin/getFirstPod.sh '+k3sMsID+'`:/var/iciclev2')
os.system('sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml  cp '+msTempD+' `'+ baseDir+'/bin/getFirstPod.sh '+k3sMsID+'`:/var/iciclev2')

#8c. Copy Microservice name and port into deployment
os.system('echo '+k3sMsID+' > '+msTempD+'/msID')
print('sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml  cp '+msTempD+'/msID `'+ baseDir+'/bin/getFirstPod.sh '+k3sMsID+'`:/var/msID')
os.system('sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml  cp '+msTempD+'/msID `'+ baseDir+'/bin/getFirstPod.sh '+k3sMsID+'`:/var/msID')
os.system('echo '+portNum+' > '+msTempD+'/msPort')
print('sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml  cp '+msTempD+'/msPort `'+ baseDir+'/bin/getFirstPod.sh '+k3sMsID+'`:/var/msPort')
os.system('sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml  cp '+msTempD+'/msPort `'+ baseDir+'/bin/getFirstPod.sh '+k3sMsID+'`:/var/msPort')
os.system('echo '+edgeNme+' > '+msTempD+'/msContext')
print('sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml  cp '+msTempD+'/msContext `'+ baseDir+'/bin/getFirstPod.sh '+k3sMsID+'`:/var/msContext')
os.system('sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml  cp '+msTempD+'/msContext `'+ baseDir+'/bin/getFirstPod.sh '+k3sMsID+'`:/var/msContext')



# 9. Install edge packages folder if applicable
# Removed July 2024
edgeDeploymentRemoved=False
if (edgeDeploymentRemoved):
    isCache=os.path.exists(edgePck+'/base')
    if (isCache):
        print('Copying the edgePackages folder into instance')
        print(baseDir + '/bin/copyFirstPod.sh ' + edgePck + '/base ' + k3sMsID)
        os.system(baseDir + '/bin/copyFirstPod.sh ' + edgePck + '/base ' + k3sMsID)
    else:   # Only this path is taken, CS July 2024
        print('The base ICICLE MS packages do not exist on this edge device')
    isCache=os.path.exists(edgePck+'/'+k3sMsID)
    if (isCache):
        print('Copying the MS-specific edgePackages folder into instance')
        print(baseDir + '/bin/copyFirstPod.sh ' + edgePck + '/' + k3sMsID + ' ' + k3sMsID)
        os.system(baseDir + '/bin/copyFirstPod.sh ' + edgePck + '/' + k3sMsID + ' ' + k3sMsID)
    else:
        print('The MS-specific packages do not exist on this edge device')        

#9b. Run startup script - Must run after edgePackages is set up to use it
print('sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml  exec -it `'+ baseDir+'/bin/getFirstPod.sh '+k3sMsID+'` -- /bin/bash /var/iciclev2/setup.sh --force')
os.system('sudo k3s kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml  exec -it `'+ baseDir+'/bin/getFirstPod.sh '+k3sMsID+'` -- /bin/bash /var/iciclev2/setup.sh --force ')
print("Completed setup.sh")
        

# 10. Check unit tests output CSV file
# 11. If failure, helm uninstall


# 12. Else, add to database as active service
    
# 13. Remove the scratch directory
os.system('rm -rf %s' % scratch)

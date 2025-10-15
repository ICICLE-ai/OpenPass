#!/bin/bash

cd /home/icicle/icicleEdge
./bin/deployMicroservice.py -home `pwd` -proxy -devel -edge edgedevel 30080website
echo Deployed Website Proxy!
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 54292openpass
echo Deployed OpenPASS!  
./bin/deployMicroservice.py -home `pwd` -devel -edge edgedevel 43210asu
echo Deployed ASU service!  


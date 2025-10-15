#!/bin/bash

INPUT=$1
if [ "$INPUT" == "" ]; then
    echo "ERROR No input provided"
    exit -1
    
fi

if [ "$INPUT" == "-" ]; then
    read -r INPUT
fi

if [ -d "/volume/devel/$INPUT/refs" ]; then
    echo "Repo exists"
    ssh stage@localhost "chmod -R 700 /volume/stage/$INPUT"    
    ssh stage@localhost "rm -rf /volume/stage/$INPUT"    
    scp -q -r /volume/devel/$INPUT stage@localhost:/volume/stage/$INPUT
    ssh stage@localhost "chmod -R 500 /volume/stage/$INPUT"
    VERSION=`cat /volume/stage/versions.txt | grep $INPUT | tail -n 1 | awk '{print $2}'`

    ((VERSION+=1))
    echo "$INPUT $VERSION" >> /volume/stage/versions.txt
else
    echo "Repo does not exist"
fi

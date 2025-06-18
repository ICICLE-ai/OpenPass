#!/usr/bin/python3

import os

def getNextId(path):
    if not os.path.isfile(path):
        id = '0'
    else:
        with open(path) as file:
            line = file.read()
            last_id = int(line)
            id = str(last_id + 1)
    
    with open(path) as file:
            file.write(id)
    



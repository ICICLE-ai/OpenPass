#!/usr/bin/python3

import os

def readPid(src):
    if src == 'local':
        path = 'latest/stream_pid.txt'
    else:
        path = '/opt/bitnami/apache/htdocs/latest/stream_pid.txt'
    
    if os.path.exists(path):
        with open(path, 'r') as file:
            pid = int(file.read())
    else:
        pid = None
    
    return pid

def writePid(src):
    if src == 'local':
        path = 'latest/stream_pid.txt'
    else:
        path = '/opt/bitnami/apache/htdocs/latest/stream_pid.txt'

    pid = os.getpid()
    with open(path, 'w+') as file:
        file.write(str(pid))
    return pid

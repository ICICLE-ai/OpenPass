#!/usr/bin/env python3

import cgitb
import urllib.request
import traceback
import os
import signal
import time
import subprocess

from Helper.UrlParameters import getUrlParameters, getNumParameters, sanitizeUrl
from Helper.PidManager import getPid, setPid, checkPid

import Helper.globals as globals

errorHTML='''<html>
<head>
</head>
<body><p> Invalid user credentials.  You can't access this page. CAUSE</p>
</body>
</html>
'''

cgitb.enable()

print('''Content-type: text/html

''')

def pingFlask(cmd):    
    cmd_url = f'http://0.0.0.0:8080/{cmd}'
    sanitized_cmd_url = sanitizeUrl(cmd_url)
    response = urllib.request.urlopen(sanitized_cmd_url)
    data = response.read()
    decoded_data = data.decode('utf-8') 
    print(decoded_data)

def runModel(): 
    flask_path = f'{globals.cgi_path}/ModelFlask.py'
    cmd = ['python3', flask_path]

    process = subprocess.Popen(cmd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        preexec_fn=(lambda: signal.signal(signal.SIGHUP, signal.SIG_IGN)))

    flask_pid = process.pid
    setPid(globals.flask_pid_path, flask_pid)

def ensureModelRunning():
    flask_pid = getPid(globals.flask_pid_path)
    if (flask_pid == -1) or (not checkPid(flask_pid)):
        print("<br>== Error: Flask Not Running ==")
        raise Exception('Error: Flask Not Running')
    else:
        print("<br>== Flask Found ==")

try: 
    #ensureModelRunning()

    print("<br>Hello World!")
    print("<br>This is the AI Missions Microservice")

    params = [getUrlParameters(f'p{i+1}', errorHTML) for i in range(getNumParameters())]
    print('<br>')
    print(params)

    setup_cmd = 'setup'
    for p in params:
        setup_cmd += f'/{p}'
    print('<br>')
    print(setup_cmd)

    print('<br><br>== (Model) | Setup Command ==')
    print('<br>')
    pingFlask(setup_cmd)

except Exception as e:
    print(f'<p>Error: {traceback.format_exc()}</p>')
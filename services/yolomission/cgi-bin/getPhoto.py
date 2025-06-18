#!/usr/bin/python3

import os
import sys
import cgitb

from Helper.UrlParameters import getUrlParameters
from Helper.IpAddress import getIpAddress
from Helper.ImgManager import ImgManager

try:
    src = sys.argv[1]    
except:
    src = 'edge'


id=None
name=None

if src != 'local':
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

    id = getUrlParameters('p1', errorHTML, error_message='No id element defined')
    name = getUrlParameters('p2', errorHTML, error_message='No name element defined')
    name = os.path.splitext(name)[0]

if (id is None): 
    if not os.path.isfile('repo/last_id.txt'):
        id = '0'
    else:
        with open('repo/last_id.txt', 'r') as file:
            line = file.read()
            last_id = int(line)
            id = str(last_id + 1)
    
    with open('repo/last_id.txt', 'w+') as file:
            file.write(id)

if (name is None):
    name = f'photo_{id}'


img_manager = ImgManager(src)
img_manager.getLatestPhoto(id, name)


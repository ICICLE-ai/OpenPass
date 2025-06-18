#!/usr/bin/python3

import sys
import cgitb

from Helper.ImgManager import ImgManager

try:
    src = sys.argv[1]    
except:
    src = 'edge'


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

img_manager = ImgManager(src)
img_manager.resetStream()

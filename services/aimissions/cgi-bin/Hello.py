#!/usr/bin/env python3

import cgitb
import os
import sys

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

try:
    print("<br>Hello World!")
    print("<br>This is the AI Missions Microservice")

    print("<br><br>Python Version:", sys.version)
    print("<br><br>System Path:", sys.path)
    print("<br><br>Current Working Directory:", os.getcwd())
    print("<br><br>Environment Variables:", os.environ)
        
except Exception as e:
    print(f'<p>Error: {e}</p>')
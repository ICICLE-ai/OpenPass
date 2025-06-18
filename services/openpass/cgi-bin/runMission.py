#!/usr/bin/env python3

import cgitb
import sys
import os

from Helper.UrlFunctions import getUrlParameters, getNumParameters
from Helper.MissionNohupFunctions import startMission

errorHTML='''<html>
<head>
</head>
<body><p> Invalid user credentials.  You can't access this page. CAUSE</p>
</body>
</html>
'''

num_params = getNumParameters()

if (num_params >= 1):
    p1 = getUrlParameters("p1", errorHTML, optional=False, error_message="No Mission File Specified")
    mission_file = f'{p1}Mission.py'
    output_file = f'{p1}Output.txt'
    image_folder = f'{p1}Img'

    p2 = getUrlParameters("p2", errorHTML, optional=True)
    if p2 == 'None':
        reset = 'true'
        num_params += 1
    else:
        reset = p2

    params = []
    if (num_params > 2):
        for i in range(num_params-2):
            p = getUrlParameters(f'p{i+3}', errorHTML)
            params.append(p)
    
else:
    errorHTML = errorHTML.replace('CAUSE', 'No mission file or output file specified')
    print(errorHTML)
    sys.exit()


# Enable CGI traceback for debugging
cgitb.enable()

print('''Content-type: text/html

''')

try:
    print(params)
    print(reset)
    process = startMission(mission_file, output_file, image_folder, reset, params)

    with open('/opt/bitnami/apache/htdocs/UpdatingPage.html', 'r') as file:
        html = file.read()
        formatted_html = html.replace('{{title}}', mission_file)
        formatted_html = formatted_html.replace('{{filename}}', output_file)
        
        print(formatted_html)

    sys.exit()
        
except Exception as e:
    print(f'<p>Error: {e}</p>')


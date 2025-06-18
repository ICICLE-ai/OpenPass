#!/usr/bin/env python3
import cgitb
import sys
import os
import json
import Helper.globals as globals
from Helper.UrlFunctions import getUrlParameters, getNumParameters
import datetime

errorHTML='''<html>
<head>
</head>
<body><p> Invalid user credentials.  You can't access this page. CAUSE</p>
</body>
</html>
'''

configfile = f"{globals.htdocs_path}/digitalagriconfig.json"


def update_json_config(token_value, dir_value, config_file_path):
    if os.path.exists(config_file_path):
        try:
            with open(config_file_path, 'r') as file:
                config_data = json.load(file)
        except json.JSONDecodeError:
            config_data = {"token": "", "dir": "", "last_updated": ""}
    else:
        config_data = {"token": "", "dir": "", "last_updated": ""}
        with open(config_file_path, 'w') as file:
            json.dump(config_data, file, indent=4)
        os.chmod(config_file_path, 0o777)
    
    config_data["token"] = token_value
    config_data["dir"] = dir_value
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config_data["last_updated"] = current_datetime
    
    # Write the updated config to the file
    with open(config_file_path, 'w') as file:
        json.dump(config_data, file, indent=4)
    
    print(json.dumps(config_data, indent=4))
    

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
    update_json_config(params[0], params[1], configfile)
        
except Exception as e:
    print(f'<p>Error: {e}</p>')


#!/usr/bin/env python3

import cgitb
import traceback
import json
import io
from contextlib import redirect_stdout

from Helper.ModelManager import ModelManager
from Helper.UrlParameters import getUrlParameters
import Helper.globals as globals

errorHTML='''<html>
<head>
</head>
<body><p> Invalid user credentials.  You can't access this page. CAUSE</p>
</body>
</html>
'''

cgitb.enable()

try:  
    target = getUrlParameters('p1', errorHTML, optional=True)

    if target == 'None':
        target = 'openpass'

    if target in globals.supported_ms:
        src_port = globals.supported_ms[target]['port']
        src_name = globals.supported_ms[target]['name']

    response_type = getUrlParameters('p2', errorHTML, optional=True)

    if response_type == 'json':
        print('''Content-type: application/json

        ''')
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            model = ModelManager(src_port, src_name)
            inference_folder = model.loadImages(True)
            result = model.Inference([inference_folder])
        print(result)
    
    else: 
        print('''Content-type: text/html

        ''')
        model = ModelManager(src_port, src_name)
        inference_folder = model.loadImages(True)
        model.Inference([inference_folder])

except Exception as e:
    if response_type is None:
        print(f'Error: {traceback.format_exc()}')
    if response_type == 'json':
        print(json.dumps({'result': False, 'message': f'Error: {traceback.format_exc()}'}))
    else:
        print(f'<p>Error: {traceback.format_exc()}</p>')
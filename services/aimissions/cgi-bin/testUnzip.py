#!/usr/bin/env python3

import cgitb
import traceback

from Helper.ModelManager import ModelManager

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
    src_port = 4242
    src_name = 'i4242phonehub'
    print('Test')

    model = ModelManager(src_port, src_name)
    model.loadImages(True)

except Exception as e:
    print(f'<p>Error: {traceback.format_exc()}</p>')

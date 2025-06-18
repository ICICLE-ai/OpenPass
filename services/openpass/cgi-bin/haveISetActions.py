#!/usr/bin/python3

import os
import cgi
import cgitb
from urllib.parse import urlparse

def is_url(url):
  try:
    result = urlparse(url)
    if (result.scheme != ''):
        return True
    return False
  except ValueError:
    return False


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

form = cgi.FieldStorage()
code = str(form.getvalue("code"))
if (code == "None"):
    errorHTML = errorHTML.replace("CAUSE","No Code element")
    print(errorHTML)
    quit()

state = str(form.getvalue("state"))
if (state == "None"):
    errorHTML = errorHTML.replace("CAUSE","No Email element")
    print(errorHTML)
    quit()
state=state.replace("@","DAB")

path = '/opt/bitnami/apache2/htdocs/userfiles/'
isExist = os.path.exists(path)
if not (isExist):
  os.makedirs(path)

path = '/opt/bitnami/apache2/htdocs/userfiles/'+state+'-demopath.txt'
isExist = os.path.exists(path)
if (isExist):
  print("\n" + "<body> True </body></html>");
else:
  print("\n" + "<body> False </body></html>");

#!/usr/bin/python3

import os
import cgi
import cgitb
import urllib.request
import dns.resolver
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
    errorHTML =replace.CAUSE("No","email element")
    print(errorHTML)
    quit()
state=state.replace("@","DAB")



path = '/opt/bitnami/apache2/htdocs/userfiles/'+state+'-waypoints.csv'
isExist = os.path.exists(path)
if (isExist):
  print("\n" + "<body> True </body></html>");
else:
  print("\n" + "<body> False </body></html>");

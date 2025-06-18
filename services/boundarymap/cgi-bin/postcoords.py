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
code= "user"
if (code == "None"):
    errorHTML = errorHTML.replace("CAUSE","No Code element")
    print(errorHTML)
    quit()

state = str(form.getvalue("state"))
state = "user"
if (state == "None"):
    errorHTML =replace.CAUSE("No","email element")
    print(errorHTML)
    quit()
state=state.replace("@","DAB")

p1val = str(form.getvalue("p1"))

#port = str(form.getvalue("port"))
# The full DNS name is default.svc.cluster.local

with open('/opt/bitnami/apache2/htdocs/userfiles/'+state+'-postcoords.txt', 'w') as file:
    file.write (p1val)


print ("<html>")
print ("<head><title>Boundary File Created Successfully</title>")
print ("<meta http-equiv=\"refresh\" content=\"10; url=https://go.osu.edu/icicle-ag\">")
print ("</head>")
print ("<body><p>The boundary file was created successfully.  You will now be redirected to our digital ag homepage</p>")
print ("</body>")
print ("</html>")

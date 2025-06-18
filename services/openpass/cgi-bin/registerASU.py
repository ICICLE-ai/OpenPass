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
    os._exit(0)

state = str(form.getvalue("state"))
if (state == "None"):
    errorHTML =errorHTML.replace("CAUSE","No email element")
    print(errorHTML)
    os._exit(0)

state=state.replace("@","DAB")

path = '/opt/bitnami/apache2/htdocs/userfiles/'
isExist = os.path.exists(path)
if not (isExist):
  os.makedirs(path)


        
with open('/etc/resolv.kube', 'r') as f:
    kubedns = str(f.read()).strip()
res = dns.resolver.Resolver(configure=False)
res.nameservers = [ kubedns ]
r = res.resolve("i43210asu.default.svc.cluster.local", 'A')
i43210asu_ipaddr = str(r[0])

# Set
with urllib.request.urlopen('http://'+i43210asu_ipaddr+':43210/cgi-bin/sendBasicCmd.py?p1=set&p2=0') as response:
   html = str(response.read())
   if "failed" in html:
     print (html)
     errorHTML =errorHTML.replace("CAUSE","Unable to execute Set command on "+ 'http://'+i43210asu_ipaddr+':43210/cgi-bin/sendBasicCmd.py?p1=set&p2=1')
     print(errorHTML)
     quit()

# Connect
with urllib.request.urlopen('http://'+i43210asu_ipaddr+':43210/cgi-bin/sendBasicCmd.py?p1=connect&p2=0') as response:
   html = str(response.read())
   if "failed" in html:
     print (html)     
     errorHTML =errorHTML.replace("CAUSE","Unable to execute Connect command")
     print(errorHTML)
     quit()

# Set Photo
with urllib.request.urlopen('http://'+i43210asu_ipaddr+':43210/cgi-bin/sendBasicCmd.py?p1=setup-photo&p2=0') as response:
   html = str(response.read())
   if "failed" in html:
     errorHTML =errorHTML.replace("CAUSE","Unable to execute Setup-Photo command")
     print(errorHTML)
     quit()     
     
path = '/opt/bitnami/apache2/htdocs/userfiles/'+state+'-registeredASU.txt'
with open(path, 'w') as file:
    file.write("<b>True</b>")

print("True</body></html>")


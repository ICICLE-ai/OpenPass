#!/usr/bin/python3

import os
import cgi
import cgitb
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
    errorHTML = errorHTML.replace("CAUSE","No Email element")
    print(errorHTML)
    quit()
state=state.replace("@","DAB")

path = '/opt/bitnami/apache2/htdocs/userfiles/'
isExist = os.path.exists(path)
if not (isExist):
  os.makedirs(path)


cmdS = str(form.getfirst("p1"))
append = str(form.getfirst("p2"))

pcnt =1
cmdArray = cmdS.split("~")
cmd=""
for parm in cmdArray:
  cmd = cmd+ "p" + str(pcnt) + "=" + parm + "&" 
  pcnt=pcnt+1
if (len(cmdArray) == 1):
      cmd = cmd + "p2=0"
#cmd = cmd+"&"+parm
#print ("cmdL " + cmd + "append " + append)


if (cmd != "None"):
  if (append != "None"):
    if (append == "0"): # Overwrite
      with open(path+state+'-demopath.txt', 'w') as file:
        file.write ( cmd + ";")
    else:
      with open(path+state+'-demopath.txt', 'a') as file:
        file.write( cmd + ";")
        
with open('/etc/resolv.kube', 'r') as f:
    kubedns = str(f.read()).strip()
res = dns.resolver.Resolver(configure=False)
res.nameservers = [ kubedns ]


with open('/opt/bitnami/apache2/htdocs/private_index.html', 'r') as file:
  private_indexHTML = file.read()

path = '/opt/bitnami/apache2/htdocs/userfiles/'+state+'-demopath.txt'
isExist = os.path.exists(path)
formHTML = ""
if (isExist):
  with open('/opt/bitnami/apache2/htdocs/userfiles/'+state+'-demopath.txt', 'r') as file:
    curdemopath = file.read()
    formHTML = "Current Path: " + curdemopath + "<br><br>"

formHTML2 = ""
with open('/opt/bitnami/apache2/htdocs/private_demomissionform.html','r') as file:
  formHTML2 = str(file.read())

private_indexHTML = private_indexHTML.replace("<!-- __ICICLE__RECORD-->", formHTML2+"<!-- __ICICLE__RECORD-->")
private_indexHTML = private_indexHTML.replace("<!-- __ICICLE__RECORD-->", formHTML)
private_indexHTML = private_indexHTML.replace("CURRENT_STATE", state)
private_indexHTML = private_indexHTML.replace("CURRENT_CODE", code)


print("\n" + private_indexHTML)


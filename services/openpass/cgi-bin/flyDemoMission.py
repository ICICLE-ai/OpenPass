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
    errorHTML =errorHTML.replace("CAUSE","No email element")
    print(errorHTML)
    quit()
state=state.replace("@","DAB")

path = '/opt/bitnami/apache2/htdocs/userfiles/'
isExist = os.path.exists(path)
if not (isExist):
  os.makedirs(path)


        
with open('/etc/resolv.kube', 'r') as f:
    kubedns = str(f.read()).strip()
res = dns.resolver.Resolver(configure=False)
res.nameservers = [ kubedns ]
r = res.resolve("i43210asu.default.svc.cluster.local")
i43210asu_ipaddr = str(r[0])
#r = res.resolve("i43210asu", 'A')
#i43210asu_ipaddr = "10.43.84.206" #str(r[0])

path = '/opt/bitnami/apache2/htdocs/userfiles/'+state+'-demopath.txt'
isExist = os.path.exists(path)
if not (isExist):
  errorHTML =errorHTML.replace("CAUSE","Can not fly demo mission - No demo path for this user")
  print(errorHTML)
  quit()


with open(path, 'r') as file:
  demopath = str(file.readline()).strip()

for cmd in demopath.split(';'):
  if "crop-model" in cmd:
    processCnt = 0
    doesProcessFileExist = os.path.exists('/opt/bitnami/apache2/htdocs/userfiles/'+state+'-processCnt.txt')
    if doesProcessFileExist:
      with open('/opt/bitnami/apache2/htdocs/userfiles/'+state+'-processCnt.txt', 'r') as f:
        processCnt = int(f.readline())
    processCnt = processCnt+1
    
    cropmodeldir = "No File Found"
    with open('/opt/bitnami/apache2/htdocs/userfiles/'+state+'-cropmodel.txt', 'r') as f:
      cropmodeldir = str(f.readline())
      cropmodeldir = cropmodeldir.strip()
    cmdurl = 'http://'+i43210asu_ipaddr+':43210/cgi-bin/sendDownloadCmd.py?p1=download'
    os.system("cp /opt/bitnami/apache2/htdocs/recent.jpg /opt/bitnami/apache2/cgi-bin/localfunctions/"+cropmodeldir+"/test")
    out = os.popen("/root/rededge/rededgecall.py "+cropmodeldir)
    print ("<br>Model output"+out)
    os.system("cp /opt/bitnami/apache2/htdocs/recent.jpg /opt/bitnami/apache2/htdocs/userfiles/"+state+"-images"+str(processCnt)+".jpg")
    with open('/opt/bitnami/apache2/htdocs/userfiles/'+state+'-processResults'+str(processCnt), 'w') as f:
      f.write("Model output"+out)
      
  elif (cmd != ''):
   print ("<br>CMD: " + cmd)
   cmdurl = 'http://'+i43210asu_ipaddr+':43210/cgi-bin/sendBasicCmd.py?'+cmd
   print ("<br>CMDURL: " + cmdurl)    
   with urllib.request.urlopen(cmdurl) as response:
     html = str(response.read())
     if "failed" in html:
       print ("<br><b>ERROR</b>:Unable to execute command" + cmd)
        
     

print("</body></html>")


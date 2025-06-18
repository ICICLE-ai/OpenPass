#!/usr/bin/python3

import os
import sys
import cgi
import cgitb
import urllib.request
import dns.resolver
from urllib.parse import urlparse

def takeoffLand(direction, ipaddr):
  try:
    cmd="p1=land&p2=0"
    if (direction == 1):
      cmd="p1=takeoff&p2=0"
    print ("<br>CMD: " + cmd)
    cmdurl = 'http://'+ipaddr+':43210/cgi-bin/sendBasicCmd.py?'+cmd
    print ("<br>CMDURL: " + cmdurl)
    with urllib.request.urlopen(cmdurl) as response:
      html = str(response.read())
      if "failed" in html:
        print ("<br><b>ERROR</b>:Unable to execute command" + cmd)
  except ValueError:
    return False
  return True

def is_url(url):
  try:
    result = urlparse(url)
    if (result.scheme != ''):
        return True
    return False
  except ValueError:
    return False

MAX_WAYPOINTS=1
SKP_WAYPOINTS=2

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
r = res.resolve("i8383boundarymap.default.svc.cluster.local")
i8383boundarymap_ipaddr = str(r[0])
#r = res.resolve("i43210asu", 'A')
#i43210asu_ipaddr = "10.43.84.206" #str(r[0])


sys.stdout.flush()
os.system("wget -O /opt/bitnami/apache2/htdocs/userfiles/"+state+"-localwaypoints.csv" + " http://"+i8383boundarymap_ipaddr+":8383/userfiles/"+state+"-waypoints.csv")

path = '/opt/bitnami/apache2/htdocs/userfiles/'+state+'-localwaypoints.csv'
isExist = os.path.exists(path)
if not (isExist):
  errorHTML =errorHTML.replace("CAUSE","Can not fly waypoint mission - unable to get waypoints from boundarymap")
  print(errorHTML)
  quit()

with open(path, 'r') as file:
  skip = 0
  ways = 0
  waypoint=""
  while (skip < SKP_WAYPOINTS):
    skip = skip + 1
    waypoint = str(file.readline()).strip()
    burn = str(file.readline()).strip()  # In the initial version of the waypoints csv from chumley there is a newline ended with ", this line reads and discards it.

  takeoffLand(1,i43210asu_ipaddr )

  while (ways < MAX_WAYPOINTS):
    ways = ways + 1
    waypoint = str(file.readline()).strip()
    burn = str(file.readline()).strip()
    data = waypoint.split(',')
    latt=data[0]
    lonj=data[1]
    zeta=data[2]
    head=data[5]
    cmd="p1=move-waypoint&p2=6&p3="+latt+"&p4="+lonj+"&p5="+zeta+"&p6=none&p7="+head+"&p8=false"
    
    print ("<br>CMD: " + cmd)
    cmdurl = 'http://'+i43210asu_ipaddr+':43210/cgi-bin/sendBasicCmd.py?'+cmd
    print ("<br>CMDURL: " + cmdurl)    
    #with urllib.request.urlopen(cmdurl) as response:
    #  html = str(response.read())
    #  if "failed" in html:
    #    print ("<br><b>ERROR</b>:Unable to execute command" + cmd)
    
     
  takeoffLand(0,i43210asu_ipaddr )
        
print("</body></html>")


#!/usr/bin/python3
from SoftwarePilot import SoftwarePilot
import time
import cgi
import cgitb
import urllib.request
import dns.resolver

cgitb.enable()
#with open('/etc/resolv.kube', 'r') as f:
#    kubedns = str(f.read()).strip()
#res = dns.resolver.Resolver(configure=False)
#res.nameservers = [ kubedns ]



# The code below is from msping
# It is left here as CGI template 
#form = cgi.FieldStorage()
#item = str(form.getvalue("ms"))
#port = str(form.getvalue("port"))
# The full DNS name is default.svc.cluster.local
#item = item + ".default.svc.cluster.local"
#r = res.resolve(item, 'A')
#ipaddr = str(r[0])
#with urllib.request.urlopen('http://'+ipaddr+':'+port+'/cgi-bin/mshello.py') as response:
#   html = response.read()

print ("Content-type: text")
print ("")




'''
This is short demo demonstrating how to connect to the drone, and execute a few basic commands
'''

sp = SoftwarePilot()

# Setup a parrot anafi drone, connected through a controller, without a specific download directory
drone = sp.setup_drone("parrot_anafi", 1, "None")

drone.connect()

#drone.piloting.takeoff()
#time.sleep(60)

# The drone will move forward 2 meters (x, y, z, angle)
#drone.piloting.move_by(2,0,0,0, wait = True)

#drone.piloting.land()

drone.disconnect()
print ("The drone is connected")
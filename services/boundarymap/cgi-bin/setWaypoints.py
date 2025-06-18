#!/usr/bin/python3

import os
import sys
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
print('''Content-type: text

''')

form = cgi.FieldStorage()
code = str(form.getvalue("code"))
if (code == "None"):
    #errorHTML = errorHTML.replace("CAUSE","No Code element")
    #print(errorHTML)
    #quit()
    print('No code specified. Defualting to "user"')
    code = "user"

state = str(form.getvalue("state"))
if (state == "None"):
    #errorHTML = errorHTML.replace("CAUSE","No email element")
    #print(errorHTML)
    #quit()
    print('No email specified. Defualting to "user"')
    state = "user"
state=state.replace("@","DAB")

pixelval = str(form.getvalue("p1"))
if (pixelval == "None"):
  pixelval="0.02"
overlapval = str(form.getvalue("p2"))
if (overlapval == "None"):
  overlapval="20"
  
#port = str(form.getvalue("port"))
# The full DNS name is default.svc.cluster.local
outString = ""
with open('/opt/bitnami/apache2/htdocs/userfiles/'+state+'-postcoords.txt', 'r') as file:
  currString = str(file.readline())
  if not currString:
    errorHTML = errorHTML.replace("CAUSE","No postcoords file")
    print(errorHTML)
    quit()
  index =0
  while ("," in currString):
    currLong, nextString = currString.split(",",1)
    currString = nextString
    if ("," in currString):
      currLatt, newString = currString.split(",",1)
      currString = newString
    else:
      currLatt = currString

    outString += currLatt+","+currLong+"\n"

with open('/opt/bitnami/apache2/htdocs/userfiles/'+state+'-postcoords-refined.txt', 'w') as file:
      file.write (outString)

with open('/opt/bitnami/apache2/htdocs/userfiles/'+state+'-waypointsinput.txt', 'w') as file:
  # Input boundary file
  file.write ("/opt/bitnami/apache2/htdocs/userfiles/"+state+"-postcoords-refined.txt" + "\n")
  file.write (pixelval + "\n")
  file.write (overlapval + "\n")    
  # Output waypoint file
  file.write ("/opt/bitnami/apache2/htdocs/userfiles/"+state+"-waypoints" + "\n")
  # Decline options in the interactive version for sorties and plots
  file.write ("n\n")
  file.write ("n\n")
  file.write ("n\n")
  file.write ("\n")
  file.write ("\n")  

sys.stdout.flush()
os.system("cd /root/FlightPathBuilder; cat /opt/bitnami/apache2/htdocs/userfiles/"+state+"-waypointsinput.txt | python3 /root/FlightPathBuilder/Build_Flight_Paths_with_Boundary.py > /dev/null ")


#Check for success 
print ("<html>")
path = '/opt/bitnami/apache2/htdocs/userfiles/'+state+'-waypoints.csv'
isExist = os.path.exists(path)
if (isExist):
  print ("<head><title>Boundary File Created Successfully</title>")
else:
  print ("<head><title>Boundary File Failed to Create.  Try again</title>")
#print ("<meta http-equiv=\"refresh\" content=\"10; url=https://go.osu.edu/icicle-ag\">")
print ("</head>")
print ("<body>")
if (isExist):
  print ("Waypoint File Created Successfully")

  # Print out boundary points
  print ("Boundary points:\n")
  with open('/opt/bitnami/apache2/htdocs/userfiles/'+state+'-postcoords.txt', 'r') as file:
    while True:
      index = 0
      currString = str(file.readline())
      if not currString:
        break
      print("Boundary coordinate %s: %s\n", (index, currString))
      index = index + 1

  # Print out waypoints
  print ("Generated waypoints:\n")
  with open('/opt/bitnami/apache2/htdocs/userfiles/'+state+'-waypoints.csv', 'r') as file:
    while True:
      index = 0
      currString = str(file.readline())
      if not currString:
        break
      print("Coordinate %s: %s\n", (index, currString))
      index = index + 1


else:
  print ("Waypoint File Failed to Create.  Try again.")
#print ("<p> You will now be redirected to our digital ag homepage</p>")
print ("</body>")
print ("</html>")



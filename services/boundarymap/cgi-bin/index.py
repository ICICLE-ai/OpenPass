#!/usr/bin/python3

import cgi
import cgitb
import urllib.request


form = cgi.FieldStorage()
#item = str(form.getvalue("ms"))
#port = str(form.getvalue("port"))
# The full DNS name is default.svc.cluster.local                                                                                                                                                                                                                                    

with urllib.request.urlopen('http://localhost:8384/index.html') as response:
   html = str(response.read().decode("utf-8"))

print ("Content-type: text/html")
print ("")
print (html)




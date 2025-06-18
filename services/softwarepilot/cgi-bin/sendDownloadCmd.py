#!/usr/bin/python3
import os
import random
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
form = cgi.FieldStorage()
cmd = str(form.getvalue("p1"))
port = 2310

os.system('curl -o /opt/bitnami/apache/htdocs/recent.jpg http://192.168.231.231:2311/recent.jpg')

print ("Content-type: text/html")
print ("")

'''
<html><body><pre>
'''
print ("Downloaded the file :")
print ("<a href=\"/recent.jpg\">Access Here</a>")
'''
Use the browser's back button to issue another command
</pre></body></html>
'''

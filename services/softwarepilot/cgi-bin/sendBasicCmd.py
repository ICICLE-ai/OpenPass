#!/usr/bin/python3
#from SoftwarePilot import SoftwarePilot
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
cmd = cmd.replace("-","/")
port = 2310

params = ""

num_params = int(form.getvalue("p2"))
if num_params > 0:
	params = "?"
	for i in range(num_params):
		p_text = "p{}".format(i+3)
		p_val = str(form.getvalue(p_text))
		params += "{}={}".format(p_text, p_val)
		if i < num_params-1:
			params += "&"
	
with urllib.request.urlopen('http://192.168.231.231:2310/'+cmd+params) as response:
   html = str(response.read())

print ("Content-type: text")
print ("")

print('''
<html><body><pre>
The selected cmd has been sent
to the drone.

''')
print("Response: "+html)

print('''
Use the browser's back button to issue another command
</pre></body></html>
''')

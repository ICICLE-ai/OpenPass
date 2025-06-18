#!/usr/bin/python3
#This code runs at reroutlab in production
# as of April 2023, Chris Stewart



import cgi
import cgitb
import subprocess
import urllib.request

cgitb.enable()
form = cgi.FieldStorage()
code = "?code="+str(form.getvalue("code"))
state = "&state="+ str(form.getvalue("state"))








a_url = "http://"
#ms_ad = subprocess.check_output(['/bin/bash','./bin/getMsAddr.sh','30080'])
a_url = a_url + str(ms_ad) + ":30080/cgi-bin/googleoauthresult.py" + code + state

print(
'''Content-type: text/html

<html>
<head>
''')
print ("<meta http-equiv=\"refresh\" content=\"2; url=\'"+a_url+"\'\" />")
print ("</head><body>Redirected</body></html>")


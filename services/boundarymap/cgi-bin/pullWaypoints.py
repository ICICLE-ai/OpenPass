#!/usr/bin/python3

import os
import sys
import cgi
import cgitb
import urllib.request
import dns.resolver
from urllib.parse import urlparse
import wget

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
state = str(form.getvalue("state"))
if (state == "None"):
    #errorHTML = errorHTML.replace("CAUSE","No email element")
    #print(errorHTML)
    #quit()
    print('No email specified. Defualting to "user"')
    state = "user"
state=state.replace("@","DAB")

print(state)

def getPodAddress(pod):
    with open('/etc/resolv.kube', 'r') as f:
        kubedns = str(f.read()).strip()
    res = dns.resolver.Resolver(configure=False)
    res.nameservers = [ kubedns ]
    r = res.resolve(f"{pod}.default.svc.cluster.local")
    ipaddr = str(r[0])

    return ipaddr



# Downloading latest coords
i54292openpass_ipaddr = getPodAddress('i54292openpass')
print(i54292openpass_ipaddr)

download_src = f"http://{i54292openpass_ipaddr}:54292/userfiles/{state}-postcoords.txt"
download_dst = f'/opt/bitnami/apache2/htdocs/userfiles/{state}-postcoords.txt'

# If old coords exist under the same name, delete them
if os.path.exists(download_dst):
   os.remove(download_dst)

# Pull coords file
filename = wget.download(download_src, out=download_dst)

print("Download Complete!")
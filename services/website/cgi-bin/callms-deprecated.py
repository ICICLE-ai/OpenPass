#!/usr/bin/python3

import os
import cgi
import shutil
import cgitb
import urllib.request
from urllib.parse import urlparse
import dns.resolver
import unicodedata
import sys
def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")


cgitb.enable()
with open('/etc/resolv.kube', 'r') as f:
    kubedns = str(f.read()).strip()
res = dns.resolver.Resolver(configure=False)
res.nameservers = [ kubedns ]

errorHTML='''Content-type: text

<html>
<head>
</head>
<body><p> Invalid user credentials.  You can't access this page. CAUSE</p>
</body>
</html>
'''

#print ("<html>")
#print ("<head></head><body>Debug</body></html>")
#quit()


form = cgi.FieldStorage()

if form.getfirst("state"):
    state = str(form.getfirst("state"))
else:
    errorHTML = errorHTML.replace("CAUSE", "Lost State")
    print (errorHTML)
    quit()
if form.getfirst("code"):
    code = str(form.getfirst("code"))
else:
    errorHTML = errorHTML.replace("CAUSE", "Lost Auth")    
    print (errorHTML)
    quit()

port = "30080"
if form.getfirst("port"):
    port = str(form.getfirst("port"))


item = "i30080website"
if form.getfirst("ms"):
    item = str(form.getfirst("ms"))
        
page = "index.html"
if form.getfirst("page"):
    page = str(form.getfirst("page"))    
    if '?' in page:
        # This is usually a cgi script with parameters
        # myscript?p1=222
        page.replace("?","&")
        
path=""
if form.getfirst("path"):
    path = str(form.getfirst("path"))

fullurl = "http://i30080website:30080/path/page?" # Note all parameters must proceed amersand &p1=xyz"
if form.getfirst("fullurl"):
    fullurl = str(form.getfirst("fullurl"))    
    o = urlparse(fullurl)
    item = o.hostname
    port = str(o.port)
    path, page = o.path.rsplit("/",1)  
    
parm=""
pcnt=1
while (pcnt < 32):
    if not (str(form.getfirst("p"+str(pcnt))) == "None"):
        parm = parm+"&p"+str(pcnt) + "="+ str(form.getfirst("p"+str(pcnt)))
    pcnt=pcnt+1


statecode = "&state=" + state + "&code=" +code

# The full DNS name is default.svc.cluster.local
item_orig = item
item = item + ".default.svc.cluster.local"
r = res.resolve(item, 'A')
ipaddr = str(r[0])
msrl='http://'+ipaddr+':'+port+'/' + path + '/'+ page + '?' + "&" + statecode + parm
msrl=remove_control_characters(msrl)
msrl=msrl.replace(" ","%20")
#msrl="http://10.43.195.204:30080/ShenKai_web.jpg"
#print (msrl)

binaryData=0
html=""
if (".txt" in msrl) or (".csv" in msrl):
    print ("Content-type: text")
    print ("")    
    with urllib.request.urlopen(msrl) as response:
        html = str(response.read().decode("utf-8"))

    binaryData=0
elif (".zip" in msrl)  or (".tar" in msrl):
    sys.stdout.buffer.write(b"Content-type: application/octet-stream\n\n")
    sys.stdout.flush()
    with urllib.request.urlopen(msrl) as response:
        shutil.copyfileobj(response, sys.stdout.buffer)
    binaryData = 1
elif (".jpg" in msrl) or (".gif" in msrl):
    sys.stdout.buffer.write(b"Content-type: image/png\n\n")
    sys.stdout.flush()
    with urllib.request.urlopen(msrl) as response:
        shutil.copyfileobj(response, sys.stdout.buffer)
    binaryData = 1
else:
    print ("Content-type: text/html")
    print ("")   
    with urllib.request.urlopen(msrl) as response:
        lt = 0
        html = str(response.read().decode("utf-8"))        
        while not ("</html>" in html):
            html = html+ str(response.readline().decode("utf-8"))
            lt = lt+1
            if (lt > 5000):
                html = html + "\n\n</html>"
    binaryData =0

if (binaryData == 0):
    # Hard links beginning with lowercase i are icicle ms names
    formUrlSwap = f"action = \"/cgi-bin/callms.PY?{statecode}&fullurl=http://i"
    html=html.replace("action=\"http://i", formUrlSwap)
    htmlUrlSwap = f"href = \"/cgi-bin/callms.PY?{statecode}&fullurl=http://i"
    html=html.replace("href=\"http://i", htmlUrlSwap)
    
    
    html=html.replace("href=\"http", "href = \" http")
    #Above: Don't want to accidently replace hard coded links
    
    cgibSwap = "href = \"/cgi-bin/callms.py?ms=" + item_orig + "&port=" + port + "&path=/cgi-bin/" + statecode + "&page="
    html=html.replace('.python?', '.py&')
    html=html.replace("href=\"/cgi-bin/", cgibSwap)

    baseSwap = "href = \"/cgi-bin/callms.py?ms=" + item_orig + "&port=" + port + "&path=/" + statecode + "&page="
    html=html.replace("href=\"/", baseSwap)

    cntxSwap = "href = \"/cgi-bin/callms.py?ms=" + item_orig + "&port=" + port + "&path=" + page + statecode + "&page="
    html=html.replace("href=\"", cntxSwap)

    formSwap = "action = \"/cgi-bin/callms.py?"
    html=html.replace("action=\"/cgi-bin/", formSwap)

    frm2Swap = "<input type = \"hidden\" name = \"state\" value = \"" + state +"\">"
    frm2Swap = frm2Swap + "<input type = \"hidden\" name = \"code\" value = \"" + code +"\"></form>"
    html=html.replace("</form>", frm2Swap)



    html=html.replace('.PY', '.py')
    html=html.replace("\\n","") #Remove new lines inserted by Python
    html=html.replace("\\t","") #Remove new lines inserted by Python
#End of if binaryData ==0

if (binaryData == 0):
    print (html)




#

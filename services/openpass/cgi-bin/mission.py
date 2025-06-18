#!/usr/bin/python3

import cgi
import cgitb
import urllib.request
import dns.resolver
from urllib.parse import urlparse

def is_url(url):
  return "cgi-bin" in url

def urlHost(url):
  try:
    result = urlparse(x)
    return str(result.host)
  except:
    return "localhost"

  
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
#code="cs"
if (code == "None"):
    errorHTML = errorHTML.replace("CAUSE","No Code element")
    print(errorHTML)
    quit()

state = str(form.getvalue("state"))
#state = "cs"
if (state == "None"):
    errorHTML = errorHTML.replace("CAUSE","No Email element")
    print(errorHTML)
    quit()

p1 = str(form.getvalue("p1"))
#p1 = "waypointmission"
if (p1 == "None"):
    errorHTML = errorHTML.replace("CAUSE","No mission type specified")
    print(errorHTML)
    quit()    


with open('/opt/bitnami/apache2/htdocs/private_index.html', 'r') as file:
    private_indexHTML = file.read()

with open('/opt/bitnami/apache2/htdocs/private_template.html', 'r') as file:
    private_templateHTML = file.read()    

readyToFly = True
curTemplate =  private_templateHTML + " "
with open('/opt/bitnami/apache2/htdocs/'+p1+'.json', 'r') as file:
    # if line is empty
    # end of file is reached
    while True:        
        curString = str(file.readline())
        if not curString:
            break
        if not ("=" in curString):
            break

        (toBeReplaced, replacement) = curString.split("=")
        replacement=replacement.strip()
        if is_url(replacement):
            #replacement = "code=" + code + "&state=" + state + "&" + replacement
            replacement = replacement + "?code=" + code + "&state=" + state
        
        if (toBeReplaced.strip() == "__ICICLE__STATUSURL"):
            status = "<b><p class=\"h5 text-danger\" data-toggle=\"tooltip\" title=\"Unknown Error\">False</p></b>"
            if (replacement.startswith("/cgi-bin")):
              try:
                with urllib.request.urlopen("http://127.0.0.1:8081/"+replacement) as response:
                  html = str(response.read())
                  if "True" in html:
                    status = "<b><p class=\"h5 text-success\" data-toggle=\"tooltip\" title=\"File found\">True</p></b>"
                  else:
                    status = "<b><p class=\"h5 text-danger\" data-toggle=\"tooltip\" title=\""+html+"\">False</p></b>"
                    readyToFly = False
              except:
                status = "<b><p class=\"h5 text-danger\" data-toggle=\"tooltip\" title=\"STATUSURL Not Defined or Inaccess\">False</p></b>"
                readyToFly = False
            else:
              try:
                with open('/etc/resolv.kube', 'r') as f:
                  kubedns = str(f.read()).strip()
                  res = dns.resolver.Resolver(configure=False)
                  res.nameservers = [ kubedns ]
                  parsedURL = urlparse(replacement)
                  item = parsedURL.hostname + ".default.svc.cluster.local"
                  r = res.resolve(item, 'A')
                  ipaddr = str(r[0])
                  
                  with urllib.request.urlopen("http://"+ipaddr+":"+str(parsedURL.port)+"/"+parsedURL.path+"?"+parsedURL.query) as response:
                    html = str(response.read())

                  if "True" in html:
                    status = "<b><p class=\"h5 text-success\" data-toggle=\"tooltip\" title=\"File found\">True</p></b>"
                  else:
                    status = "<b><p class=\"h5 text-danger\" data-toggle=\"tooltip\" title=\""+html+"\">False</p></b>"
                    readyToFly = False
              except:
                status = "<b><p class=\"h5 text-danger\" data-toggle=\"tooltip\" title=\"STATUSURL Not Defined or Inaccess\">False</p></b>"
                readyToFly = False
              
            replacement = status
                
        curTemplate = curTemplate.replace(toBeReplaced, replacement)
        if (toBeReplaced.strip() == "__ICICLE__ENDRECORD"):
            curTemplate = curTemplate + "\n<!-- __ICICLE__RECORD-->"
            private_indexHTML = private_indexHTML.replace("<!-- __ICICLE__RECORD-->", curTemplate)
            curTemplate = private_templateHTML + " "  

if (readyToFly == False):
    private_indexHTML = private_indexHTML.replace("<!-- __ICICLE__READYTOFLY-->", "<nav class=\"navbar navbar-expand-lg navbar-dark text-danger bg-warning\"> <p class=\"navbar-text text-danger\" href=\"#\"><b>NOT READY TO FLY</b></a>  </nav>")
else:
    private_indexHTML = private_indexHTML.replace("<!-- __ICICLE__READYTOFLY-->", "<nav class=\"navbar navbar-expand-lg navbar-dark bg-success\"> <p class=\"navbar-text text-dark\" href=\"#\"><b>READY.  Click Fly</b></p>  </nav>")
print("\n" + private_indexHTML)


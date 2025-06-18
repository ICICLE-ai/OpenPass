#!/usr/bin/python3

import cgi
import cgitb
from urllib.parse import urlparse
import unicodedata

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")
  
def is_url(url):
  return "cgi-bin" in url


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
code = str(form.getvalue("code")).strip()
#code= "cs"
if (code == "None"):
  errorHTML = errorHTML.replace("CAUSE","No Code element")
  print(errorHTML)
  quit()
  
state = str(form.getvalue("state")).strip()
#state="cs"
if (state == "None"):
  errorHTML = errorHTML.replace("CAUSE","No Email element")
  print(errorHTML)
  quit()


with open('/opt/bitnami/apache2/htdocs/private_setcropmodel.html', 'r') as file:
  private_indexHTML = file.read()

with open('/opt/bitnami/apache2/htdocs/private_cropmodel_template.html', 'r') as file:
  private_templateHTML = file.read()    

curTemplate =  private_templateHTML + " "
with open('/opt/bitnami/apache2/htdocs/cropModels.json', 'r') as file:
  # if line is empty
  # end of file is reached
  while True:        
    curString = str(file.readline())
    if not curString:
      break
    if not ("=" in curString):
      break
    (toBeReplaced, replacement) = curString.split("=",1)
    replacement=replacement.strip()
    
    if is_url(replacement):
        replacement = replacement + "?code=" + code + "&state=" + state
    
    curTemplate = curTemplate.replace(toBeReplaced, replacement)
    if (toBeReplaced.strip() == "__ICICLE__ENDRECORD"):
        curTemplate = curTemplate + "\n<!-- __ICICLE__RECORD-->"
        private_indexHTML = private_indexHTML.replace("<!-- __ICICLE__RECORD-->", curTemplate)
        curTemplate = private_templateHTML + " "  
      
print("\n" + private_indexHTML)


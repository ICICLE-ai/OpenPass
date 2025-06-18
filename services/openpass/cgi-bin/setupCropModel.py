#!/usr/bin/python3

import os
import cgi
import cgitb
import urllib.request
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
#code ="cs"
if (code == "None"):
    errorHTML = errorHTML.replace("CAUSE","No Code element")
    print(errorHTML)
    quit()

state = str(form.getvalue("state"))
#state="cs"
if (state == "None"):
    errorHTML =errorHTML.replace("CAUSE","No Email element")
    print(errorHTML)
    quit()
state=state.replace("@","DAB")


modelname = str(form.getvalue("p1"))
if (modelname == "None"):
  modelname="EmptyName"
modeldescription = str(form.getvalue("p2"))
if (modeldescription == "None"):
  modeldescription=""
modelurl = str(form.getvalue("p3"))
if (modelurl == "None"):
  modelurl=""  
modelexec = str(form.getfirst("p4"))
modeltestinput = str(form.getfirst("p5"))
if (modelexec == "None") or (modelexec == "Default"):
  modelexec="""
#!/usr/bin/python3

import cv2
import tensorflow as tf
import numpy as np
from keras.preprocessing.image import img_to_array
import time
import os
from flask import Flask,jsonify

app = Flask(__name__)

model = tf.keras.models.load_model("model")

@app.route('/exec', methods=['GET'])
def exec():
  img = cv2.imread("test")
  img = cv2.resize(img, (108, 108))
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  img = img.astype('float') / 255.0
  img = img_to_array(img)
  img = np.expand_dims(img, axis=0)
  acc = model.predict(img)[0][1]
  acc = round(acc, 4)
  return jsonify({'output': str(acc)})
@app.route('/unload', methods=['GET'])
def unload():
  os._exit(0)
  os.system("rm -r " + __ICICLE__MODELPATH)
  return jsonify({'output': 'unloaded'})
@app.route('/load', methods=['GET'])
def load():
  return jsonify({'output': 'loaded'})

"""


# 1. Create /opt/bitnami/apache2/cgi-bin/openwhisk/localfunctions/"state"-modelname/inputs.txt
# This file will replicate inputs above and add additional parameters needed for rededge
path = '/opt/bitnami/apache2/cgi-bin/localfunctions/'+state+'-'+modelname+'/'
modelexec=modelexec.replace("__ICICLE__MODELPATH",path)


# 1a. #Remove all previous models by the user

os.system('rm -r /opt/bitnami/apache2/htdocs/userfiles/'+state+'-cropmodel.txt')
os.system("rm -r " + path)
os.system("mkdir " + path)
os.system("chmod 777 " + path)
inptFle = path + 'inputs.txt'
with open(inptFle, 'w') as file:
  file.write("modelname="+modelname+"\n")
  file.write("modeldescription="+modeldescription+"\n")    
  file.write("modelurl="+modelurl+"\n")
  file.write("modelexec="+modelexec+"\n")
  file.write("modeltestinput="+modeltestinput+"\n")        

#2. Download all models and inputs to the said directory
print("wget --no-check-certificate --output-file="+path+"model.log " + " -O " +path+"model \"" + modelurl +"\"" )
os.system("wget --no-check-certificate --output-file="+path+"model.log "+ " -O " +path+"model \"" + modelurl +"\""  )
if not (modeltestinput == "None"):
  print("wget --no-check-certificate --output-file="+path+"test.log "+ " -O " +path+"test \"" + modeltestinput+"\""  )
  os.system("wget --no-check-certificate --output-file="+path+"test.log "+ " -O " +path+"test \"" + modeltestinput+"\""  )
with open(path+"exec.py", 'w') as file:
  file.write(modelexec)

# 3. Call rededge to launch faas function
os.system("chmod 777 -R " + path)
with urllib.request.urlopen('http://localhost:7787/rededgelaunch?name='+modelname+'&dir='+path) as response:
   html = response.read()
print (html)

chkFle = '/opt/bitnami/apache2/htdocs/userfiles/'+state+'-cropmodel.txt'
with open(chkFle, 'w') as file:
  file.write(state+'-'+modelname)

print ("Crop model is setup")




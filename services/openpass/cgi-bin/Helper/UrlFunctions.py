import cgi
import os
from urllib.parse import parse_qs, urlencode

def getUrlParameters(param_name, errorHTML, optional=False, error_message='No Parameter Specified'): 
    form = cgi.FieldStorage()
    param = str(form.getvalue(param_name))
    if (not optional) and (param == "None"):
        errorHTML = errorHTML.replace("CAUSE", error_message)
        print(errorHTML)
        quit() 
    return param

def getNumParameters():
    form = cgi.FieldStorage()
    count = sum(1 for key in form.keys() if key.startswith('p'))
    return count

def addUrlParameter(key, value):
    query_string = os.environ.get('QUERY_STRING', '')
    params = parse_qs(query_string)

    params[key] = [value]
    new_query_string = urlencode(params, doseq=True)

    base_url = os.environ.get('SCRIPT_NAME', '')
    base = base_url.split('/')
    full_url = f'http://10.43.195.204:30080/cgi-bin/callms.py?ms=i54292openpass&port=54292&path=/{base[1]}/&page={base[2]}&{new_query_string}'
    
    return full_url
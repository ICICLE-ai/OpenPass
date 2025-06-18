import cgi

def getUrlParameters(param_name, errorHTML, optional=False, error_message='No Parameter Specified'): 
    form = cgi.FieldStorage()
    param = str(form.getvalue(param_name))
    if (not optional) and (param == "None"):
        errorHTML = errorHTML.replace("CAUSE", error_message)
        print(errorHTML)
        quit() 
    return param


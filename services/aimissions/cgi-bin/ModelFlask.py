from markupsafe import escape
from flask import Flask
import traceback
import os
import importlib
import traceback

from Models.Yolo import Yolo
from Helper.PidManager import setPid
import Helper.globals as globals


local = False
if local:
    repo_path = globals.local_repo_path
else:
    repo_path = globals.repo_path
in_path = f'{repo_path}/in'
out_path = f'{repo_path}/out'

model = None
current_model_class = None
current_model_weights = None

app = Flask(__name__)
print("READY!")


@app.route("/")
def index():
    try:
        return {
            'result': True,
            'values': 'Hello World!'
        }
    except Exception as e:
        print(f'Error: {traceback.format_exc()}')
        return { 
            'result': False, 
            'values': traceback.format_exc()
        }


@app.route("/setup/<string:model_class>/<string:model_weights>")
def setup(model_class, model_weights):
    global model, current_model_class, current_model_weights

    print("Weights setup route")
    try:
        if (current_model_class is None) or (current_model_weights is None) or (current_model_class != model_class) or (current_model_weights != model_weights):
            
                module = importlib.import_module(f'Models.{model_class}')
                model = getattr(module, model_class)(model_weights)
                current_model_class = model_class
                current_model_weights = model_weights
                
                print(model)
                print(current_model_class)
                print(current_model_weights)

        result = {
            'result': True,
            'values': {
                'model': current_model_class,
                'weights': current_model_weights
            }
        }
        return result
        
    except Exception as e:
        print(f'Error: {traceback.format_exc()}')
        return { 
            'result': False, 
            'values': traceback.format_exc()
        }

@app.route("/setup/<string:model_class>/<string:model_weights>/<path:varargs>")
def setup_varargs(model_class, model_weights, varargs):
    global model, current_model_class, current_model_weights

    print("Weights setup route")
    try:
        varargs = varargs.split('/')
        for i in range(len(varargs)):
            print(f'Arg #{i}: {varargs[i]}')

        module = importlib.import_module(f'Models.{model_class}')
        model = getattr(module, model_class)(model_weights, *varargs)
        current_model_class = model_class
        current_model_weights = model_weights
        
        print(model)
        print(current_model_class)
        print(current_model_weights)

        result = {
            'result': True,
            'values': {
                'model': current_model_class,
                'weights': current_model_weights,
                'var_args': varargs
            }
        }
        return result
        
    except Exception as e:
        print(f'Error: {traceback.format_exc()}')
        return { 
            'result': False, 
            'values': traceback.format_exc()
        }

@app.route("/setup/<string:model_class>")
def setup_no_weights(model_class):
    global model, current_model_class, current_model_weights

    print("No Weights setup route")
    try:
        if (current_model_class is None) or (current_model_class != model_class):          

            module = importlib.import_module(f'Models.{model_class}')
            model = getattr(module, model_class)()
            current_model_class = model_class
            current_model_weights = None
            
            print(model)
            print(current_model_class)
            print(current_model_weights)

        result = {
            'result': True,
            'values': {
                'model': current_model_class,
                'weights': current_model_weights
            }
        }
        return result

    except Exception as e:
        print(f'Error: {traceback.format_exc()}')
        return { 
            'result': False, 
            'values': traceback.format_exc()
        }

@app.route("/inference/<path:varargs>")
def inference(varargs=None):
    global model

    if model is None:
        return {
            'result': False,
            'values': 'ERROR: Missing model'
        }

    try:
        varargs = varargs.split('/')
        for i in range(len(varargs)):
            print(f'Arg #{i}: {varargs[i]}')

        response = model.Inference(*varargs)
        return response
       
    except Exception as e:
        print(f'Error: {traceback.format_exc()}')
        return { 
            'result': False, 
            'values': traceback.format_exc()
        }

@app.route("/inference")
def basicInference():
    global model

    if model is None:
        return {
            'result': False,
            'values': 'ERROR: Missing model'
        }

    try:
        response = model.Inference()
        return response
       
    except Exception as e:
        print(f'Error: {traceback.format_exc()}')
        return { 
            'result': False, 
            'values': traceback.format_exc()
        }


if __name__ == "__main__":
    from waitress import serve
    flask_pid = os.getpid()
    setPid(globals.flask_pid_path, flask_pid)
    serve(app, host="0.0.0.0", port=8080)

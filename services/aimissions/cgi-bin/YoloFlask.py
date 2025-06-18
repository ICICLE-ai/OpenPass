from markupsafe import escape
from flask import Flask
import traceback
import os

from Models.Yolo import Yolo
import Helper.globals as globals


local = False
if local:
    repo_path = globals.local_repo_path
else:
    repo_path = globals.repo_path
in_path = f'{repo_path}/in'
out_path = f'{repo_path}/out'

yolo = Yolo()
print("READY!")

app = Flask(__name__)


@app.route("/")
def index():
    try:
        return {
            'result': True,
            'values': 'Hello World!'
        }
    except:
        return { 
            'result': False, 
            'values': traceback.format_exc()
        }

@app.route("/test/<string:target_img>/<string:new_img>")
def test(target_img, new_img):
    try:
        
        img_path = f"{in_path}/{escape(target_img)}"
        download_path = f"{out_path}/{escape(new_img)}"

        result = {
            'result': True,

            'values': {
                'img_path': img_path,
                'download_path': download_path
            }
        }
        return result
    
    except:
        return { 
            'result': False, 
            'values': traceback.format_exc()
        }

@app.route("/inference/<string:target_img>/<string:new_img>")
def inference(target_img, new_img):
    try:

        img_path = f"{in_path}/{escape(target_img)}"
        download_path = f"{out_path}/{escape(new_img)}"
        
        if not os.path.exists(img_path):
            raise Exception(f'Invalid image path {img_path}')

        yolo.objectInference(img_path, download_path)

        if not os.path.exists(download_path):
            raise Exception(f'Failed image storage {download_path}')

        result = {
            'result': True,

            'values': {
                'download_path': download_path
            }
        }
        return result
       
    except:
        return { 
            'result': False, 
            'values': traceback.format_exc()
        }

@app.route("/inference/<string:target_img>/<string:new_img>/<string:target>")
def inferenceTarget(target_img, new_img, target):
    try:

        img_path = f"{in_path}/{escape(target_img)}"
        download_path = f"{out_path}/{escape(new_img)}"

        if not os.path.exists(img_path):
            raise Exception(f'Invalid image path {img_path}')

        bounding_box, offset_x, offset_y, img_shape = yolo.objectInference(img_path, download_path, target_label=target)
        
        if not os.path.exists(download_path):
            raise Exception(f'Failed image storage {download_path}')

        result = {
            'result': True,

            'values': {
                'download_path': download_path,
                'bounding_box': bounding_box,
                'offset_x': offset_x,
                'offset_y': offset_y,
                'img_shape': img_shape
            }
        }
        return result
       
    except:
        return { 
            'result': False, 
            'values': traceback.format_exc()
        }
    
@app.route("/correct/<string:target_img>/<string:new_img>/<string:target>/<float:alt>")
def correctTarget(target_img, new_img, target, alt):
    try:
        
        img_path = f"{in_path}/{escape(target_img)}"
        download_path = f"{out_path}/{escape(new_img)}"
        
        if not os.path.exists(img_path):
            raise Exception(f'Invalid image path {img_path}')

        bounding_box, offset_x, offset_y, img_shape = yolo.objectInference(img_path, download_path, target_label=target)
        correction_x, correction_y = Yolo.calculateMeterCorrection(offset_x, offset_y, img_shape, alt)

        if not os.path.exists(download_path):
            raise Exception(f'Failed image storage {download_path}')

        result = {
            'result': True,

            'values': {
                'download_path': download_path,
                'bounding_box': bounding_box,
                'correction_x': correction_x,
                'correction_y': correction_y        
            }
        }
        return result
       
    except:
        return { 
            'result': False, 
            'values': traceback.format_exc()
        }


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
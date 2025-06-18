#!/usr/bin/python3

import os
import urllib.request

from Helper.AddressFunctions import getPodAddress
import Helper.globals as globals


class AIManager:
    def __init__(self, image_folder):
        self.image_subpath = f'{globals.userfiles_path}/{image_folder}'
        self.model_name = None
        self.model_script = None

        self.ai_port = 1212
        self.ai_ipaddr = getPodAddress('i1212aimissions')
        self.base_cmd = f'http://{self.ai_ipaddr}:{self.ai_port}'
        
        self.in_path = f'{globals.mscopy_path}/model_in.jpg'
        self.out_path = f'{globals.userfiles_path}/model_out.jpg'

    def runModel(self, img_name):
        if self.model_name is None:
            return '<br>ERROR: model is not defined'

        img_path = f'{self.image_subpath}/{img_name}'
        
        result = f'<br>== Prepping image to {self.model_name} =='
        copy_cmd = f'cp {img_path} {self.in_path}' 
        result += f'<br>CMD: {copy_cmd}'
        os.system(copy_cmd)   
        
        result += f'<br>== Sending inference cmd to {self.model_name} =='
        run_cmd = f'{self.base_cmd}/cgi-bin/{self.model_script}'
        result += f'<br>CMDURL: {run_cmd}'
        
        response = urllib.request.urlopen(run_cmd)
        data = response.read()
        decoded_data = data.decode('utf-8') 
        
        result += decoded_data

        return result

    def getImage(self, download_name):
        if self.model_name is None:
            return '<br>ERROR: model is not defined'
        
        download_path = f'{self.image_subpath}/{download_name}'

        result = f'<br>== Retrieving image from {self.model_name} =='
        src_url = f'{self.base_cmd}/mscopy/model_out.jpg'
        result += f'<br>CMDURL: {src_url}'
        
        file, header = urllib.request.urlretrieve(src_url, self.out_path)
    
        result += '<br>== Copying image to mission folder =='
        copy_cmd = f'cp {self.out_path} {download_path}' 
        result += f'<br>CMD: {copy_cmd}'
        os.system(copy_cmd)   

        return result, file, header

    def Inference(self, img_name, download_name):
        if self.model_name is None:
            return '<br>ERROR: model is not defined'
        
        model_result = self.runModel(img_name)
        image_result, file, header = self.getImage(download_name)
        result = model_result + image_result
        return result, file, header

    def Setup(self, model_name, model_weights=None):
        self.model_name = model_name
        self.model_weights = model_weights
        self.model_script = f'run{model_name}.py'

        result = f'<br>== Setting up model {self.model_name} ==' 
        cmd = f'{self.base_cmd}/cgi-bin/Setup.py?p1={self.model_name}'
        if model_weights is not None:
            cmd += f'&p2={self.model_weights}'
        result += f'<br>CMDURL: {cmd}'
        
        response = urllib.request.urlopen(cmd)
        data = response.read()
        decoded_data = data.decode('utf-8') 
        
        result += decoded_data

        return result
#!/usr/bin/env python3

import os
import sys
import urllib.request
import io
from contextlib import redirect_stdout

from Helper.ZipFunctions import unzipFile
from Helper.UrlParameters import sanitizeUrl
from Helper.PodAddress import getPodAddress
from Helper.CopyFunctions import CopyMSTo
import Helper.globals as globals

class ModelManager:
    def __init__(self, src_port, src_name):
        self.mscopy_in_path = f'{globals.mscopy_path}/{globals.in_file}'
        self.mscopy_out_path = f'{globals.mscopy_path}/{globals.out_file}'
        self.image_folder = None 
        
        self.src_port = src_port
        self.src_name = src_name
        self.src_ipaddr = getPodAddress(src_name)
        self.pull_suburl = f'http://{self.src_ipaddr}:{self.src_port}/mscopy'

        self.base_cmd = 'http://0.0.0.0:8080'

    def pingFlask(self, cmd):
        cmd_url = f'{self.base_cmd}/{cmd}'
        sanitized_cmd_url = sanitizeUrl(cmd_url)
        response = urllib.request.urlopen(sanitized_cmd_url)
        data = response.read()
        decoded_data = data.decode('utf-8')
        print(f'<br>Result: {decoded_data}')
        return decoded_data

    def pullImage(self):
        pull_url = f'{self.pull_suburl}/{globals.in_file}'

        print('<br>== (Model) | Loading Images ==')
        
        print(f'CMDURL: {pull_url}')
        file, header = urllib.request.urlretrieve(pull_url, self.mscopy_in_path)
        
        cp_cmd = f'cp {self.mscopy_in_path} {globals.in_path}'
        print(f'CMD: {cp_cmd}')
        os.system(cp_cmd)

        return file, header

    def unzipImages(self):
        src_dir = f'{globals.zipDir_path}'

        files = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]

        if not files:
            return None
        
        youngest_file = max(files, key=os.path.getmtime)
        self.image_folder = os.path.splitext(os.path.basename(youngest_file))[0]
        dst_path = f'{globals.repo_path}/{self.image_folder}'
        os.makedirs(dst_path, exist_ok=True)
    
        unzipFile(youngest_file, dst_path)
        return self.image_folder

    def loadImages(self, is_zip=False):
        if is_zip:
            return self.unzipImages()
        else:
            file, header = pullImage()
            return file, header

    def Inference(self, params=None):
        print('<br>== (Model) | Running Inference ==')
        cmd = 'inference'
        if params is not None:
            for param in params:
                cmd += f'/{param}'
        
        print(f'<br>CMD: {cmd}')
        print(f'<br>CMDURL: {self.base_cmd}/{cmd}')
        data = self.pingFlask(cmd)
        
        if self.src_name == globals.supported_ms['openpass']['name']:
            print('<br>== (Model) | Prepping Results Transfer ==')
            cp_cmd = f'cp {globals.out_path} {self.mscopy_out_path}'
            print(f'CMD: {cp_cmd}')
            os.system(cp_cmd)
       
        else:
            print('<br>== (Model) | Sending Results ==')
            for file_name in os.listdir(globals.result_path):               
                print(f'<br>-- Copying {file_name} --')

                src_path = f'{globals.result_path}/{file_name}'
                download_dir = globals.supported_ms['phone']['path']
                dst_path = f'{download_dir}/{file_name}'

                print(f'<br>SRC Path: {src_path}')
                print(f'<br>DST Path: {self.src_name}:{dst_path}')

                success = CopyMSTo(self.src_port, self.src_name, src_path, dst_path)
                if success:
                    result = f'<br>Successfully Copied {src_path} to {self.src_name}:{dst_path}'
                else:
                    result = f'<br>Error: Failed to copy {src_path}'

        return data
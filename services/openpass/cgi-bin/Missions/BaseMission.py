#!/usr/bin/python3

import time
import os
import traceback
import sys
import requests
import json
import datetime

sys.path.append('/opt/bitnami/apache/cgi-bin')
from Helper.DroneManager import DroneManager
from Helper.ImageManager import ImageManager
from Helper.TimeoutFunctions import run_with_timeout
from Helper.UrlFunctions import addUrlParameter
import Helper.globals as globals

class BaseMission:
    def __init__(self):
        self.mission_file = os.path.basename(sys.argv[0])
        self.output_file = sys.argv[1]
        self.image_folder = sys.argv[2]
        self.reset = (sys.argv[3] == 'true')

        self.progress_file = f'{os.path.splitext(self.mission_file)[0]}Progress.json'
        self.progress_path = f'{globals.htdocs_path}/{self.progress_file}'
        self.output_path = f'{globals.htdocs_path}/{self.output_file}'
        self.tapis_config_path = f'{globals.htdocs_path}/digitalagriconfig.json'

        self.images = ImageManager(self.image_folder)
        self.download_dir = self.images.getPath()
        self.drone = DroneManager(self.download_dir)
        self.last_completed = 0

        if self.reset:
            self.images.reset()
            self.writef('Resetting Images')
        
        if os.path.exists(self.tapis_config_path):
            self.writef("<br>====== TAPIS Credentials found.......Initiating Digital Agriculture Mode ======")
        else:
            self.writef("<br>====== Running on normal mode to enable Digital Agriculture mode add credentials first ======")

    def writef(self, str):
        with open(self.output_path, 'a') as file:
            file.write(str)
            
    def stopf(self):
        time.sleep(globals.wait)
        self.writef('STOP')

    def timed(self, func, params, timeout=globals.timeout, optional=True):
        result = run_with_timeout(func, params, timeout)

        if result == 'TIMEOUT':
            if optional:
                result = '<br>=!= Function Timed Out. Skipping. =!='
            else:
                self.writef('<br>=!= Fatal Function Timed Out. Exiting. =!=')
                self.drone.stopStreamCommand()
                sys.exit()
        
        return result

    def download_and_display_image(self, img_name, wait=True, timed=False):
        if wait:
            time.sleep(globals.wait)
        if timed:
            self.writef(self.timed(self.drone.downloadStreamCommand, [img_name, None]))
            self.writef(self.timed(self.images.display_image, [img_name]))
        else:
            self.writef(self.drone.downloadStreamCommand(img_name, None))
            self.writef(self.images.display_image(img_name))

    def upload_folder(self, tk, destination_path, filename):
        jwt_token = f"{tk}"
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        source_folder_path = f'/opt/bitnami/apache/htdocs/userfiles/{filename}/'
        url = f"https://icicleai.tapis.io/v3/files/ops/{destination_path}/{filename}_{current_time}/"
        
        for root, dirs, files in os.walk(source_folder_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, source_folder_path)
                dest_url = url + "/" + relative_path.replace("\\", "/")
                headers = {
                    "X-Tapis-Token": jwt_token
                }
                files = {
                    "file": open(local_file_path, "rb")
                }
                response = requests.post(dest_url, headers=headers, files=files)
                if response.status_code != 200:
                    self.writef(f"<br>=====Failed to upload {local_file_path}: {response.text}====")
        
        return "Folder upload completed"

    def baseStart(self, stream=True, takeoff=True, imagecapture=False):
        self.writef(f'<br><br>== Start {self.mission_file} ==')
        
        self.writef('<br><br>== Connecting to the Drone ==')
        self.writef(self.drone.sendCommand('p1=set&p2=0'))
        self.writef(self.drone.sendCommand('p1=connect&p2=0'))

        if stream:
            self.writef('<br><br>== Starting Stream ==')
            self.writef(self.drone.startStreamCommand())
            self.download_and_display_image('start.jpg')

        if takeoff:
            self.writef('<br><br>== Taking Off ==')
            self.writef(self.drone.sendCommand('p1=takeoff&p2=0'))
            self.download_and_display_image('takeoff.jpg')

            self.readProgress()
        
        if imagecapture:
            self.writef('<br><br>== Setting Up Image Capture Mode ==')
            self.writef(self.drone.sendCommand('p1=setup-photo&p2=0'))

    def baseEnd(self, stream=True, takeoff=True, stopPrinting=True):
        if takeoff:
            self.writef('<br><br>== Landing ==')
            self.writef(self.drone.sendCommand('p1=land&p2=0'))
            self.download_and_display_image('land.jpg')
        
        if stream:
            self.writef('<br><br>== Stopping Stream ==')
            self.writef(self.drone.stopStreamCommand())

        self.writef('<br><br>== Disconnecting from the Drone ==')
        self.writef(self.drone.sendCommand('p1=disconnect&p2=0'))

        self.writef(f'<br><br>== End {self.mission_file} ==')

        self.writef(self.images.link_download_zip(self.image_folder))

        if stopPrinting:
            self.stopf()

    def updateCompleted(self):
        self.last_completed += 1
        self.writef(f'<br>== Mission Checkpoint {self.last_completed} ==')

    def writeProgress(self):
        data = {
            'last_completed': self.last_completed,
            'errorred_position': self.drone.relative_position 
        }

        with open(self.progress_path, 'w') as file:
            json.dump(data, file)

    def readProgress(self):
        if (not self.reset) and os.path.exists(self.progress_path):
            with open(self.progress_path, 'r') as file:
                data = json.load(file)
                self.last_completed = data['last_completed']
                errorred_position = data['errorred_position']

                self.writef('<br><br>== Moving to Last Position ==')
                self.writef(self.drone.moveCommand(*errorred_position, angle=0, wait=True))
        else:
            self.last_completed = 0

    def restartMission(self, stream, takeoff):
        try:
            self.writeProgress()

            self.writef("<br><br>== Aborting mission ==")
            self.writef('<br><br>== Returning to Start ==')
            self.writef(self.drone.returnHome())
            
            self.baseEnd(stream, takeoff, stopPrinting=False)

            new_url = addUrlParameter('p2', 'false')

            self.writef('<br><br>')
            self.writef(f'<a href = "{new_url}">')
            self.writef('<button type="submit">Restart</button>')
            self.writef('</a>')
            
            self.stopf()

        except Exception:
            var = traceback.format_exc()
            self.writef(var)

    # Ensure Printing Error Trace
    def run(self, mission, stream=True, takeoff=True):
        try:
            mission()
        except Exception:
            var = traceback.format_exc()
            self.writef(var)
            self.restartMission(stream, takeoff)

    def enableDigitalAgriculture(self):
        config_path = self.tapis_config_path
        if not os.path.exists(config_path):
            self.writef("<br><br>== Config file not found enabling normal mode. Exiting digital agriculture mode ==")
            return False
        else:
            response = []
            response.append(True)
            with open(config_path, "r") as file:
                config_data = json.load(file)
            
                response.append(config_data["token"])
                response.append(config_data["dir"])
                
            response.append(self.image_folder)

            self.writef(f"<br><br>== Tapis Initialization Started..... Fetched the config file: {response}")
            return response
        
    def captureImage(self):
        # foldername = f"{self.image_folder}_{current_time}"
        # folderpath = f"{globals.userfiles_path}/{foldername}"
        # os.mkdir(folderpath)
        try:
            self.writef('<br><br>== Capturing Image ==')
            self.writef(self.drone.sendCommand('p1=take-photo&p2=0'))
            self.writef(self.drone.sendCommand(f'p1=download&p2=0'))
        except Exception:
            var = traceback.format_exc()
            self.writef(var)

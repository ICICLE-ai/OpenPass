#!/usr/bin/python3

import os
import stat
import time
import json
import shutil

LOCAL = "/home/icicle/icicleEdge/yolomission"
EDGE = "/opt/bitnami/apache2/htdocs"

class ImgManager:
    def __init__(self, src='edge', reset=False):
        self.src = src
        if src == "local":
            self.latest_dir = f"{LOCAL}/latest"
            self.repo_dir = f"{LOCAL}/repo"
        else:
            self.latest_dir = f"{EDGE}/latest"
            self.repo_dir = f"{EDGE}/repo"
        self.stream_flag = f"{self.latest_dir}/stream_flag.txt"

        if reset:
            self.resetPhoto()
            self.resetStream()

    def resetPhoto(self):
        self.resetTarget("photo")
    
    def resetStream(self):
        self.resetTarget("stream")

    def resetTarget(self, target):
        path = f"{self.repo_dir}/{target}"
        data_file = f'{path}/{target}_data.json'
        
        if os.path.exists(path):
            shutil.rmtree(path)
            time.sleep(1)

            os.makedirs(path, exist_ok=True)
            permissions = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO  # 0o777
            os.chmod(path, permissions)

        with open(data_file, 'w') as file:
            data = json.loads("{}")
            json.dump(data, file, indent=4)

    def updatePhotoFile(self, id, new_data):
        self.updateFile("photo", id, new_data)
    
    def updateStreamFile(self, id, new_data):
        self.updateFile("stream", id, new_data)

    def updateFile(self, target, id, new_data):
        latest_path = f'{self.latest_dir}/{target}/latest_{target}_data.json'
        with open(latest_path, 'r+') as file:
            # Load Photo data from file
            photo_data = json.load(file)
            
            # Update Photo date
            photo_data['id'] = id 

            # Save Photo data to file
            file.seek(0)
            json.dump(photo_data, file, indent=4)
        
        repo_path = f"{self.repo_dir}/{target}/{target}_data.json"
        with open(repo_path, 'r+') as file:
            # Load Photo data from file
            data = json.load(file)
            
            # Update Photo date
            data[id] = new_data

            # Save Photo data to file
            file.seek(0)
            json.dump(data, file, indent=4)


    def getLatestPhoto(self, id, download_name):
        self.getLatest("photo", id, download_name)
    
    def getLatestStream(self, id, download_name):
        self.getLatest("stream", id, download_name)

    def getLatest(self, target, id, download_name):
        if target == "photo":
            update = self.updatePhotoFile
        elif target == "stream":
            update = self.updateStreamFile
        else:
            return False
        
        latest_path = f"{self.latest_dir}/{target}/latest_{target}"
        repo_path = f"{self.repo_dir}/{target}/{download_name}"
        
        # Download latest photo + data, and store as latest
        os.system(f'curl -o {latest_path}.jpg http://192.168.231.231:2311/{target}.jpg')
        os.system(f'curl -o {latest_path}_data.json http://192.168.231.231:2311/{target}_data.json')
        
        # Update the photo repository
        os.system(f'cp {latest_path}.jpg {repo_path}.jpg')
        new_data = self.getNewData(f"{latest_path}_data.json", f"{repo_path}.jpg")
        update(id, new_data)
        print(f"\n== Downloaded latest {target} as {download_name}! ==")

        return True
        
    def getNewData(self, json_path, img_path):
        with open(json_path, 'r') as file:
            new_data = json.load(file)
            new_data["path"] = img_path
        
        return new_data

    def startStream(self):
        # If a previous stream exists, kill it
        self.stopStream()

        # Write stream active to file
        with open(self.stream_flag, 'w+') as file:
            file.write('True')        

        # Start stream
        print('\n== Starting New Img Stream ==')
        counter = 0
        stream = True
        while stream:
            self.getLatestStream(counter, f'stream_{counter}')
            time.sleep(1)
            counter += 1
            
            # Check for termination
            with open(self.stream_flag, 'r') as file:
                flag = file.read()
                if flag != 'True':
                    stream = False

    def stopStream(self):
        if os.path.exists(self.stream_flag):
            with open(self.stream_flag, 'w') as file:
                file.write('False')
                print('\n== Stopped Img Stream ==')
        else:
            print('\n== No Img Stream Found. Skipping ==')
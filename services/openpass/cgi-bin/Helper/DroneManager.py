import os
import re
import ast
import requests
import urllib.request
import threading
import time

from Helper.AddressFunctions import getPodAddress
from urllib.error import HTTPError


class DroneManager:
    def __init__(self, download_dir):
        self.asu_ipaddr = getPodAddress('i43210asu')
        self.repo_ipaddr = getPodAddress('i2222yolomissions')
        
        self.asu_port = 43210
        self.repo_port = 2222

        self.download_dir = download_dir
        self.stream = None

        self.relative_position = [0,0,0]
        self.start_coord = None

    def command(self, ipaddr, port, cmd):
        result = f'<br>CMD: {cmd}'
        cmdurl = f'http://{ipaddr}:{port}/{cmd}'  
        result += f'<br>CMDURL: {cmdurl}'
        
        response = requests.get(cmdurl)
        get_response = response.text
        if "failed" in get_response:
            result += f'<br><b>ERROR</b>:Unable to execute command {cmd}'
        response.close()
        
        return result, get_response
    
    def sendCommand(self, cmd):
        refined_cmd = f'cgi-bin/sendBasicCmd.py?{cmd}'
        result, _= self.command(self.asu_ipaddr, self.asu_port, refined_cmd)
        
        return result
    
    def valueCommand(self, cmd, key):
        refined_cmd = f'cgi-bin/sendBasicCmd.py?{cmd}'
        result, get_response= self.command(self.asu_ipaddr, self.asu_port, refined_cmd)
        parsed_response = ast.literal_eval(re.search('({.+})', get_response).group(0))
        value = parsed_response[key]
        
        return result, value

    def coordCommand(self):
        try:
            coord_result, start_coord = self.valueCommand('p1=get-coordinates&p2=0', 'coordinates')
        except:
            coord_result = "<br>== Failed to get drone coordinates =="
            start_coord = [500.0, 500.0, 500.0]

            #'''
            lat = 40.0089852740562
            lon = -83.01683790675908
            alt = 5

            start_coord = [lat, lon, alt]
            #'''

        return coord_result, start_coord

    def moveCommand(self, x, y, z, angle, wait):
        cmd = f'p1=move-distance&p2=5&p3={x}&p4={y}&p5={z}&p6={angle}&p7={wait}'
        
        self.relative_position[0] += int(x)
        self.relative_position[1] += int(y)
        self.relative_position[2] += int(z)

        result = self.sendCommand(cmd)
        
        return result

    def waypointCommand(self, lat, lon, alt, heading, wait):
        if self.start_coord is None:
            _, self.start_coord = self.coordCommand()

        result = '<br><br>-------- Flying To --------'
        result += f'<br>Lat: {lat}'
        result += f'<br>Lon: {lon}'
        result += f'<br>Alt: {alt}'
        result += f'<br>Heading: {heading}'
        result += '<br>'

        cmd = f'p1=move-waypoint&p2=6&p3={lat}&p4={lon}&p5={alt}&p6=NONE&p7={heading}&p8={wait}'
        result += self.sendCommand(cmd)

        return result

    def startStreamCommand(self):
        result = self.sendCommand('p1=setup-streaming&p2=8&p3=2&p4=False&p5=None&p6=None&p7=None&p8=None&p9=None&p10=None')
        result += self.sendCommand('p1=take-streaming-start&p2=0')

        stream_start_cmd = 'cgi-bin/startStream.py'
        self.stream = threading.Thread(target=self.command, args=(self.repo_ipaddr, self.repo_port, stream_start_cmd))
        
        result += f'<br>CMD: {stream_start_cmd}'
        cmdurl = f'http://{self.repo_ipaddr}:{self.repo_port}/{stream_start_cmd}'  
        result += f'<br>CMDURL: {cmdurl}'
        
        self.stream.start()

        return result

    def stopStreamCommand(self):
        result = self.sendCommand('p1=take-streaming-stop&p2=0')
        
        # Check if stream is active
        if self.stream is None:
            result += "<br>== No Active Stream. Skipping =="
        else:
            # Send stop command to the repo
            stream_stop_cmd = 'cgi-bin/stopStream.py'
            command_result, _ = self.command(self.repo_ipaddr, self.repo_port, stream_stop_cmd)
            
            result += command_result
            
            self.stream = None

        return result
            
    def downloadPhotoCommand(self, download_name, img_id=None):
        result = self.sendCommand('p1=take-photo&p2=0')
        result += '<br>== Taking photo =='

        if (img_id is None):
            upload_cmd = 'cgi-bin/getPhoto.py'
            img_name = 'latest_photo.jpg'
            repo_path = f'latest/photo/{img_name}'
        else:
            upload_cmd = f'cgi-bin/getPhoto.py?p1={img_id}'
            img_name = f'photo_{img_id}.jpg'
            repo_path = f'repo/photo/{img_name}'
       
        download_path = f'{self.download_dir}/{download_name}'
        
        # Upload photo from drone to our image repo microservice
        download_result, _ = self.command(self.repo_ipaddr, self.repo_port, upload_cmd)
        result += download_result
        result += f'<br>== Uploaded {img_name} to image repo =='

        # Download photo from our image repo microservice to current microservice      
        self.download(download_path, repo_path)
        result += f'<br>== Downloaded {img_name} as {download_name} from image repo =='

        return result

    def downloadStreamCommand(self, download_name, img_id=None):
        if (img_id is None):
            img_name = 'latest_stream.jpg'
            repo_path = f'latest/stream/{img_name}'
        else:
            img_name = f'stream_{img_id}.jpg'
            repo_path = f'repo/stream/{img_name}'
        
        download_path = f'{self.download_dir}/{download_name}'
        
        # Download stream frame from our image repo microservice to current microservice
        self.download(download_path, repo_path)
        result = f'<br>== Downloaded {img_name} as {download_name} =='

        return result

    def download(self, download_path, repo_path):
        file, _ = urllib.request.urlretrieve(f'http://{self.repo_ipaddr}:{self.repo_port}/{repo_path}', download_path)
        '''
        timeout = time.time() + 2
        while (not os.path.exists(download_path)) or (os.path.getsize(download_path) == 0):
            try:
                file, _ = urllib.request.urlretrieve(f'http://{self.repo_ipaddr}:{self.repo_port}/{repo_path}', download_path)
            except HTTPError as e:
                continue
            
            if time.time() > timeout:
                print('<br>== Img Download Timed Out, Skipping == ')
                break
        '''

    def returnHome(self):
        if self.start_coord is None:
            return_move = [-1*x for x in self.relative_position]
            result = self.moveCommand(return_move[0], return_move[1], return_move[2], angle=0, wait=True)
        else:
            result = self.waypointCommand(self.start_coord[0], self.start_coord[1], 5, heading=0, wait=True)

        return result
    
#!/usr/bin/python3
import time
import sys
from BaseMission import BaseMission
mission = BaseMission()

def fullMission():

    mission.baseStart(takeoff=False)
    
    # == Stream ==
    for i in range(10):
        if mission.last_completed <= i:
            mission.writef(f'<br><br>== Downloading Image {i} ==')
            image_name = f'stream_{i}.jpg'
            mission.download_and_display_image(image_name, wait=False)
            time.sleep(1)
        mission.updateCompleted()
    # == Stream ==
    
    mission.baseEnd(takeoff=False)
    if mission.enableDigitalAgriculture():
        parameters = mission.enableDigitalAgriculture()
        mission.upload_folder(parameters[1], parameters[2], parameters[3])


mission.run(fullMission)
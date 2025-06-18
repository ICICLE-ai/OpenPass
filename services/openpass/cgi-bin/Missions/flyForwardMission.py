#!/usr/bin/python3

import sys

from BaseMission import BaseMission

mission = BaseMission()

def fullMission():

    size = sys.argv[4]

    mission.baseStart()

    # == Move Forward ==
    mission.writef(f'<br><br>== Moving Forward {size} Meters ==')
    mission.writef(mission.drone.moveCommand(size, 0, 0, 0, True))
    mission.download_and_display_image('move.jpg')
    # == Move Forward ==
    
    mission.baseEnd()
    if mission.enableDigitalAgriculture():
        parameters = mission.enableDigitalAgriculture()
        mission.upload_folder(parameters[1], parameters[2], parameters[3])

mission.run(fullMission)
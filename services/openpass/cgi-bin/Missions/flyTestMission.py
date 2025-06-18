#!/usr/bin/python3

from BaseMission import BaseMission

mission = BaseMission()

def fullMission():
    
    mission.baseStart()
    mission.baseEnd()
    if mission.enableDigitalAgriculture():
        parameters = mission.enableDigitalAgriculture()
        mission.upload_folder(parameters[1], parameters[2], parameters[3])
    

mission.run(fullMission)
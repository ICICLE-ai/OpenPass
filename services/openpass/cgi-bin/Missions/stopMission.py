#!/usr/bin/python3

import time

from BaseMission import BaseMission
from Helper.MissionNohupFunctions import stopPrevMission

mission = BaseMission()

def fullMission():
   
    mission.writef('<br>==Stopping Previous Mission==')
    mission.stopf()
    

mission.run(fullMission, takeoff=False)
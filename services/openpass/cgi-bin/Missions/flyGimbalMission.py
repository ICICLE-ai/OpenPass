#!/usr/bin/python3

from BaseMission import BaseMission

mission = BaseMission()

def fullMission():
    
    mission.baseStart(takeoff=False, stream=False)

    mission.writef('<br><br>== Setting Gimbal ==')
    mission.writef(mission.drone.sendCommand('p1=setup-orientation&p2=0&p3=0&p4=-90&p4=0&p5=True'))
    
    mission.baseEnd(takeoff=False, stream=False)

mission.run(fullMission)
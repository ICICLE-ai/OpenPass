#!/usr/bin/python3

from BaseMission import BaseMission
import sys
from Helper.AddressFunctions import getPodAddress
import math
import csv
import requests

mission = BaseMission()

def fullMission():
    drone = mission.drone
    mission.writef('<br><br>== Starting Mission ==')
    mission.writef(mission.timed(drone.sendCommand, ['p1=connect&p2=0']))

    mission.writef('<br><br>== Landing ==')
    mission.writef(drone.sendCommand('p1=land&p2=0'))
    mission.baseEnd(takeoff=False,stream=False)

    smartfieldip = "10.42.0.15"
    response = requests.get(f"http://{smartfieldip}:5001/callback?step=step3")
    mission.writef(f'{response}')


mission.run(fullMission)
#!/usr/bin/python3

import sys

from BaseMission import BaseMission

mission = BaseMission()

def fullMission():
    
    size = float(sys.argv[4])

    mission.baseStart()

    # == Square ==
    move = size

    if mission.last_completed <= 0:
        mission.writef(f'<br>== Moving 1-0 ==')
        mission.writef(mission.drone.moveCommand(move, 0, 0, 0, True))
        mission.download_and_display_image('stream_1-0.jpg')
        mission.updateCompleted()

    if mission.last_completed <= 1:
        mission.writef(f'<br>== Moving 1-1 ==')
        mission.writef(mission.drone.moveCommand(0, move, 0, 0, True))
        mission.download_and_display_image('stream_1-1.jpg')
        mission.updateCompleted()

    move *= -1

    if mission.last_completed <= 2:
        mission.writef(f'<br>== Moving 0-1 ==')
        mission.writef(mission.drone.moveCommand(move, 0, 0, 0, True))
        mission.download_and_display_image('stream_0-1.jpg')
        mission.updateCompleted()

    if mission.last_completed <= 3:
        mission.writef(f'<br>== Moving 0-0 ==')
        mission.writef(mission.drone.moveCommand(0, move, 0, 0, True))
        mission.download_and_display_image('stream_0-0.jpg')
        mission.updateCompleted()
    # == Square ==

    mission.baseEnd()
    if mission.enableDigitalAgriculture():
        parameters = mission.enableDigitalAgriculture()
        mission.upload_folder(parameters[1], parameters[2], parameters[3])


mission.run(fullMission)
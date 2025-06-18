#!/usr/bin/python3

import sys

from BaseMission import BaseMission

mission = BaseMission()

def fullMission():   
    size = float(sys.argv[4])
    grid_size = int(sys.argv[5])
    grid_distance = size/grid_size
    
    mission.baseStart()

    # == Lawnmower ==
    move_vertical = grid_distance
    move_horizontal = grid_distance

    mission.writef(f'<br> Move Vertical: {move_vertical}')
    mission.writef(f'<br> Move Horizontal: {move_horizontal}')
    
    index_vertical = 0
    index_horizontal = 0
    step = 1

    counter = 0
    while index_horizontal < grid_size:

        for i in range(grid_size):            
            index_vertical += step
            
            if mission.last_completed <= counter:
                mission.writef(f'<br><br>== Moving {index_vertical}-{index_horizontal} ==')
                mission.writef(mission.drone.moveCommand(move_vertical, 0, 0, 0, True))
                mission.download_and_display_image(f'stream_{index_vertical}-{index_horizontal}.jpg')
                mission.updateCompleted()
            
            counter += 1
            
        step *= -1
        move_vertical *= -1
        index_horizontal += 1

        if mission.reset and mission.last_completed >= 10:
            raise RuntimeError('Raise Runtime Error')

        if mission.last_completed <= counter:
            mission.writef(f'<br><br>== Moving {index_vertical}-{index_horizontal} ==')
            mission.writef(mission.drone.moveCommand(0, move_horizontal, 0, 0, True))
            mission.download_and_display_image(f'stream_{index_vertical}-{index_horizontal}.jpg')
            mission.updateCompleted()
        
        counter += 1

    mission.writef('<br><br>== Moving To Start ==')
    mission.writef(mission.drone.returnHome())
    mission.download_and_display_image('return.jpg')
    # == Lawnmower ==

    mission.baseEnd()
    if mission.enableDigitalAgriculture():
        parameters = mission.enableDigitalAgriculture()
        mission.upload_folder(parameters[1], parameters[2], parameters[3])


mission.run(fullMission)
#!/usr/bin/python3

import sys
import math

from BaseMission import BaseMission

sys.path.append('/opt/bitnami/apache/cgi-bin')
from Helper.GPSFunctions import drawSquare

mission = BaseMission()

def fullMission():

    size = int(sys.argv[4])
    drone = mission.drone

    mission.baseStart(takeoff=False)

    # == Waypoint Square ==

    # Get Drone's starting coordinates and orientation
    #'''
    coord_result, start_coord = drone.coordCommand()
    mission.writef(coord_result)
    heading_result, heading_rad = drone.valueCommand('p1=get-heading&p2=0', 'heading')
    mission.writef(heading_result)
    heading = math.degrees(heading_rad) % 360
    
    '''
    lat = 40.0089852740562
    lon = -83.01683790675908
    alt = 5
    heading = 0

    start_coord = [lat, lon, alt]
    #'''

    if 500.0 in start_coord:
        mission.writef('<br><br><b>ERROR</b>: Attempting to fly indoors. Please move outside and try again.')
    else:
        # Draw the Square and print out its boundary coordinates
        mission.writef(f"<br><br> Drone's Current Coordinate: {start_coord}")
        mission.writef(f"<br><br> Drone's Current Heading: {heading}")
        mission.writef(f"<br><br> Chose Square Size: {size}ft.")
        mission.writef(f"<br><br> Drawing Square from Current Coordinate and Heading")

        square_coordinates = drawSquare(start_coord, size, heading)
        
        counter = 0
        for coord in square_coordinates:
            mission.writef(f"<br> Coordinate #{counter}:    {coord[0]} {coord[1]}")
            counter += 1
        
        # Set Gimbal
        mission.writef('<br><br>== Setting Gimbal ==')
        mission.writef(mission.drone.sendCommand('p1=setup-orientation&p2=0&p3=0&p4=-90&p4=0&p5=True'))

        # Fly the mission
        mission.writef('<br><br>== Taking Off ==')
        mission.writef(mission.timed(drone.sendCommand, ['p1=takeoff&p2=0']))
        mission.download_and_display_image('takeoff.jpg')

        # If restarting, returning to starting position
        mission.readProgress()

        counter = 0
        for coord in square_coordinates:
            lat = coord[0]
            lon = coord[1]
            
            if mission.reset and mission.last_completed == 2:
                raise RuntimeError('Raising Runtime Error')

            if mission.last_completed <= counter:
                mission.writef(f'<br><br>== Waypoint #{counter+1} ==')

                mission.writef(drone.waypointCommand(lat, lon, 5, heading, True))
                img_name_waypoint = f'waypoint_{lat}_{lon}.jpg'
                mission.download_and_display_image(img_name_waypoint)
                mission.updateCompleted()
            
            counter += 1

        mission.writef('<br><br>== Returning to Start ==')
        mission.writef(mission.drone.returnHome())
        mission.download_and_display_image('return.jpg')

        mission.writef('<br><br>== Landing ==')
        mission.writef(drone.sendCommand('p1=land&p2=0'))
        mission.download_and_display_image('land.jpg')

    # == Waypoint Square == 

    mission.baseEnd(takeoff=False)
    if mission.enableDigitalAgriculture():
        parameters = mission.enableDigitalAgriculture()
        mission.upload_folder(parameters[1], parameters[2], parameters[3])

mission.run(fullMission)
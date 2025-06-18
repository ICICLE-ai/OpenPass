#!/usr/bin/python3

import sys
import time
import os
import math
import pandas as pd

from BaseMission import BaseMission

sys.path.append('/opt/bitnami/apache/cgi-bin')
from Helper.GPSFunctions import drawSquare
from Helper.AddressFunctions import getPodAddress
from Helper.GLIFunctions import getGLI
from Helper.FoliumFunctions import createHeatMap
from Helper.ResponseFunctions import getDecodedResponse, pullFile

import Helper.globals as globals

mission = BaseMission()

def fullMission():
  pixelval = float(sys.argv[4])
  overlapval = float(sys.argv[5])
  size = int(sys.argv[6])

  # TODO Fix user
  state = 'user'

  drone = mission.drone

  # == Setup ==

  # Print params
  mission.writef(f'<br>state:    {state}')
  mission.writef(f'<br>size:    {size}')
  mission.writef(f'<br>pixelval:    {pixelval}')
  mission.writef(f'<br>overlapval:    {overlapval}')

  # Get the ip address of the boundarymap pod
  i8383boundarymap_ipaddr = getPodAddress('i8383boundarymap')

  # Create postcoords file and give proper permissions
  coordinate_path = f'{globals.userfiles_path}/{state}-postcoords.txt'
  if not os.path.isfile(coordinate_path):
    os.system(f'touch {coordinate_path}')
    os.system(f'chmod 777 {coordinate_path}')

  mission.baseStart(takeoff=False)

  # == Waypoint Lawnmower ==

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

    # Write the boundary coordinates to {state}-postcoords.txt file
    with open(coordinate_path, 'w') as file:     
      counter = 0
      num_coord = len(square_coordinates)
      
      for coord in square_coordinates:
          mission.writef(f"<br> Coordinate #{counter}:    {coord[0]} {coord[1]}")
          counter += 1
          
          file.write(f'{coord[1]},{coord[0]}')
          if (counter < num_coord):
              file.write(',')
      
    # Push initial coordinates to the boundarymap ms
    mission.writef('<br><br>== Pushing Boundary Waypoints ==')
    pushWaypoints_url = f'http://{i8383boundarymap_ipaddr}:8383/cgi-bin/pullWaypoints.py?&code=user&state=user'
    decoded_data = getDecodedResponse(pushWaypoints_url)
    print(decoded_data)
    
    # Set waypoints using John's code
    mission.writef('<br><br>== Generating Waypoint Path ==')
    generatePath_url = f'http://{i8383boundarymap_ipaddr}:8383/cgi-bin/setWaypoints.py?&code=user&state=user'
    decoded_data = getDecodedResponse(generatePath_url)
    print(decoded_data)

    time.sleep(globals.wait)

    # Pull the lawnmower coordinates
    mission.writef('<br><br>== Pulling Waypoint File ==')
    src_url = f'http://{i8383boundarymap_ipaddr}:8383/userfiles/{state}-waypoints.csv'
    dst_path = f'/opt/bitnami/apache2/htdocs/userfiles/{state}-waypoints.csv'
    pullFile(src_url, dst_path)

    # Open Waypoint Path CSV file
    waypoints_path = dst_path
    SKP_WAYPOINTS = 2
    with open(waypoints_path, 'r') as file:
      
      # Skip csv file headers
      for i in range(SKP_WAYPOINTS):
        first_line = file.readline()
        mission.writef(f'SKIP LINE: {first_line}')

      # Set camera orientation to down
      mission.writef('<br><br>== Setting Gimbal ==')
      mission.writef(mission.drone.sendCommand('p1=setup-orientation&p2=0&p3=0&p4=-90&p4=0&p5=True'))

      mission.writef('<br><br>== Taking Off ==')
      mission.writef(mission.drone.sendCommand('p1=takeoff&p2=0'))
      mission.download_and_display_image('takeoff.jpg')

      # If restarting, returning to starting position
      mission.readProgress()

      # Initializing Heatmap DF
      heat_df = pd.DataFrame(columns=['lat', 'lon', 'gli'])
      image_folder_path = mission.images.getPath()

      # Core Loop: Fly to each waypoint and take an image
      counter = 0
      for line in file:
        if line.strip() != '"':
          values = line.split(',')
          lat = values[0]
          lon = values[1]
          #alt = values[2]
          alt = 5
          heading = values[5]

          mission.writef(f'<br><br>== Waypoint #{counter+1} ==')

          img_name_waypoint = f'waypoint_{lat}_{lon}.jpg'
          #'''
          if mission.last_completed <= counter:
            mission.writef(drone.waypointCommand(lat, lon, alt, heading, True))
            mission.download_and_display_image(img_name_waypoint)
            mission.updateCompleted()
          #'''

          # Evaluate GLI
          image_path = f'{image_folder_path}/{img_name_waypoint}'
          gli = getGLI(image_path)

          #Record Heatmap DF row
          row = [float(lat), float(lon), gli]
          heat_df.loc[counter] = row

          mission.writef(f'<br> {row}')

          counter += 1
      
      createHeatMap(heat_df, 'gli')
  
      mission.writef('<br><br>== Returning to Start ==')
      mission.writef(drone.returnHome())
      mission.download_and_display_image('return.jpg')
      
      mission.writef('<br><br>== Landing ==')
      mission.writef(drone.sendCommand('p1=land&p2=0'))
      mission.download_and_display_image('land.jpg')

  # == Waypoint Lawnmower == 

  mission.baseEnd(takeoff=False, stopPrinting=False)

  # Vizualize Data
  map_url = f'http://10.43.195.204:30080/cgi-bin/callms.py?ms=i54292openpass&port=54292&path=/&state=user&code=user&page=gps_waypoints_map.html'
  mission.writef('<br><br>')
  mission.writef(f'<a href = "{map_url}">')
  mission.writef('<button type="submit">Vizualize Waypoints</button>')
  mission.writef('</a>')

  mission.stopf()
  if mission.enableDigitalAgriculture():
    parameters = mission.enableDigitalAgriculture()
    mission.upload_folder(parameters[1], parameters[2], parameters[3])


mission.run(fullMission)
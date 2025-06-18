#!/usr/bin/python3

import sys
import time
import os
import urllib.request
import folium

from urllib.error import HTTPError
from BaseMission import BaseMission

sys.path.append('/opt/bitnami/apache/cgi-bin')
from Helper.GPSFunctions import drawSquare
from Helper.AddressFunctions import getPodAddress
import Helper.globals as globals

mission = BaseMission()

def fullMission():
  pixelval = float(sys.argv[4])
  overlapval = float(sys.argv[5])
  size = int(sys.argv[6])

  # TODO Fix user
  state = 'user'

  # == Setup ==

  # Print params
  mission.writef(f'<br>state:    {state}')
  mission.writef(f'<br>size:    {size}')
  mission.writef(f'<br>pixelval:    {pixelval}')
  mission.writef(f'<br>overlapval:    {overlapval}')

  # Get the ip address of the boundarymap pod
  i8383boundarymap_ipaddr = getPodAddress('i8383boundarymap')
  #print(f'i8383boundarymap_ipaddr:    {i8383boundarymap_ipaddr}')

  # Create postcoords file and give proper permissions
  coordinate_path = f'{globals.userfiles_path}/{state}-postcoords.txt'
  if not os.path.isfile(coordinate_path):
    os.system(f'touch {coordinate_path}')
    os.system(f'chmod 777 {coordinate_path}')

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
    push_response = urllib.request.urlopen(f'http://{i8383boundarymap_ipaddr}:8383/cgi-bin/pullWaypoints.py?&code=user&state=user')
    mission.writef('<br><br>== Pushed Postcoords.txt ==')
    data = push_response.read()
    decoded_data = data.decode('utf-8') 
    mission.writef(decoded_data)
    
    # Set waypoints using John's code
    set_response = urllib.request.urlopen(f'http://{i8383boundarymap_ipaddr}:8383/cgi-bin/setWaypoints.py?&code=user&state=user')
    mission.writef('<br><br>== Set Waypoints ==')
    data = set_response.read()
    decoded_data = data.decode('utf-8') 
    mission.writef(decoded_data)
    
    time.sleep(globals.wait)

    # Pull the lawnmower coordinates
    waypoints_path = f'/opt/bitnami/apache2/htdocs/userfiles/{state}-waypoints.csv'
    while (not os.path.exists(waypoints_path)) or (os.path.getsize(waypoints_path) == 0):
      try:
        file, _ = urllib.request.urlretrieve(f'http://{i8383boundarymap_ipaddr}:8383/userfiles/{state}-waypoints.csv', waypoints_path)
      except HTTPError as e:
        continue
    mission.writef('<br><br>== Pulled Waypoints.csv ==')

    SKP_WAYPOINTS = 2
    with open(waypoints_path, 'r') as file:
      # Skip headers
      for i in range(SKP_WAYPOINTS):
        first_line = file.readline()
        mission.writef(f'SKIP LINE: {first_line}')

      # Fly to each waypoint and take an image
      counter = 0
      for line in file:
        if line.strip() != '"':
          values = line.split(',')
          lat = values[0]
          lon = values[1]
          #alt = values[2]
          alt = 5
          heading = values[5]

          if counter == 0:
            map_center = (lat, lon)
            mymap = folium.Map(location=map_center, zoom_start=6)

          folium.Marker(location=[lat, lon]).add_to(mymap)
          counter += 1

      mymap.save("gps_waypoints_map.html")

  # == Waypoint Lawnmower == 

mission.run(fullMission)
#!/usr/bin/python3

from BaseMission import BaseMission
from Helper.AcerLandParameter import get_waypoints
import Helper.globals as globals
import csv
from io import StringIO
import time
import math
                                                                                                                            
mission = BaseMission()

def fullMission():

    # Establishing Connection
    mission.baseStart(takeoff=False,stream=False,imagecapture=True)

    # Connecting to drone
    drone = mission.drone

    # Getting current drone coordinate
    start_coord, current_coordinates = drone.coordCommand()

    # Getting heading of the drone
    heading_result, heading_rad = drone.valueCommand('p1=get-heading&p2=0', 'heading')
    mission.writef(f"{heading_result}")
    heading = math.degrees(heading_rad) % 360

    # Desired location (Location from where you want location to start)
    desired_cordinates = [40.008002333334815, -83.0186213333282]

    mission.writef(f"<br><br>== Current Coordinates: {current_coordinates}==")
    if current_coordinates[0] is 40.0089852740562:
        mission.writef("<br><br> Default Coordinates Identified....")
        mission.writef("<br><br> Abborting....")
        mission.stopf()

    # Creating the drone flight path
    side = "A"
    waypoints, csv_data, map_obj, line_spacing, photo_spacing, photo_interval_time, photos_per_line, num_lines, width_meters, height_meters = get_waypoints(desired_cordinates,side)

    # Displaying the drone planner
    mission.writef(f"<br><br>Input: Corner {side.upper()} at [{desired_cordinates[0]:.8f}, {desired_cordinates[1]:.8f}]")
    mission.writef(f"<br> Field Dimensions: {width_meters:.1f}m x {height_meters:.1f}m ({width_meters * height_meters:.0f} sq meters)")
    mission.writef(f"<br> Flight Lines: {num_lines}")
    mission.writef(f"<br> Photos per Line: {photos_per_line}")
    mission.writef(f"<br> Total Waypoints: {len(waypoints)}")
    mission.writef(f"<br> Estimated Flight Time: {len(waypoints) * photo_interval_time / 60:.1f} minutes")
    mission.writef(f"<br> Line Spacing: {line_spacing:.1f}m")
    mission.writef(f"<br> Photo Spacing: {photo_spacing:.1f}m")
    mission.writef(f"<br> Map created with satellite view and interactive features")

    # Saving required assets
    map_directory = f"{globals.userfiles_path}/OrthomosiacMap.html"
    csv_directory = f"{globals.userfiles_path}/OrthomosiacCSV.csv"

    map_obj.save(map_directory)
    mission.writef(f"\nInteractive map saved as 'OrthomosiacMap.html'")
    mission.writef("Open this file in your browser to view the satellite map with flight path!")

    # Creating a CSV file of coordinates
    input_csv = StringIO(csv_data)
    reader = csv.DictReader(input_csv)
    with open(csv_directory, 'w', newline='') as f:
        fieldnames = ['Waypoint', 'Latitude', 'Longitude', 'Altitude_AGL_m', 'Action', 'Photo_Interval_s']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for row in reader:
            if row['Action'] == 'PHOTO':
                writer.writerow(row)

    iframe = map_obj._repr_html_()

    html_content = f"<br><br><div style='width: 700; height: 400;'>{iframe}</div>"

    # Displaying the drone planner in a map form
    mission.writef(html_content)

    # Taking Off
    mission.writef('<br><br>== Taking Off ==')
    mission.writef(mission.timed(drone.sendCommand, ['p1=takeoff&p2=0']))

    mission.writef('<br><br>== Starting Mission ==')

    # Starting with the mission and covering all the point for mission
    with open(csv_directory, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mission.writef(f"<br><br> Waypoint: {row['Waypoint']}, Latitude: {row['Latitude']}, Longitude: {row['Longitude']}, Altitude: {row['Altitude_AGL_m']}, Action: {row['Action']}")
            mission.writef(drone.waypointCommand(row['Latitude'], row['Longitude'], row['Altitude_AGL_m'], heading, True))
            mission.writef(mission.timed(drone.sendCommand, ['p1=take-photo&p2=0']))
            mission.writef(mission.timed(drone.sendCommand, ['p1=download&p2=0']))
            time.sleep(1)

    mission.writef("<br><br>== All waypoints completed ==")

    # Returning back to home location
    mission.writef("<br><br>== Returning back to the home location ==")
    mission.writef(drone.waypointCommand(current_coordinates[0], current_coordinates[1], 30, heading, True))

    # Landing the drone
    mission.writef('<br><br>== Landing ==')
    mission.writef(drone.sendCommand('p1=land&p2=0'))

    # Disconnecting from the drone
    mission.baseEnd(takeoff=False,stream=False)

mission.run(fullMission)
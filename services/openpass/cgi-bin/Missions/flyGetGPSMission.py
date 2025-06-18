#!/usr/bin/python3

from BaseMission import BaseMission
import Helper.globals as globals
from datetime import datetime
import csv

mission = BaseMission()


def fullMission():

    mission.baseStart(takeoff=False, stream=False)
    drone = mission.drone
    start_coord, coord_result = drone.coordCommand()
    # coord_result = [39.99263458457224, -83.0088499831398, 5]
    mission.writef(f"{coord_result}")
    if coord_result[0] is 40.0089852740562:
        mission.writef("<br><br> Default Coordinates Identified....")
        mission.writef("<br><br> Abborting....")
        mission.stopf()

    mission.writef(f"<br><br> Drone's Current Coordinate: {coord_result}")

    fetch_coordinate_csv = f"{globals.userfiles_path}/get_coordinates_timestamp.csv"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(fetch_coordinate_csv, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([coord_result[0],coord_result[1],coord_result[2], timestamp])

    mission.baseEnd(takeoff=False, stream=False)

mission.run(fullMission)
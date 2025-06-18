# #!/usr/bin/python3

# from BaseMission import BaseMission
# import sys
# import math
# import csv
# import Helper.globals as globals

# mission = BaseMission()

# def fullMission():

#     lat = sys.argv[4]
#     long = sys.argv[5]
#     alt = 10

#     mission.baseStart(takeoff=False,stream=False)

#     fetch_coordinate_csv = f"{globals.userfiles_path}/smartfield_coordinates.csv"
#     drone = mission.drone
#     start_coord, coord_result = drone.coordCommand()
#     with open(fetch_coordinate_csv, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(coord_result[:2])
#     heading_result, heading_rad = drone.valueCommand('p1=get-heading&p2=0', 'heading')
#     mission.writef(heading_result)
#     heading = math.degrees(heading_rad) % 360
#     mission.writef(f"{coord_result}")
#     if coord_result[0] is 40.0089852740562:
#         mission.writef("<br><br> Default Coordinates Identified....")
#         mission.writef("<br><br> Abborting....")
#         mission.stopf()

#     mission.writef(f"<br><br> Drone's Current Coordinate: {coord_result}")

#     mission.writef('<br><br>== Taking Off ==')
#     mission.writef(mission.timed(drone.sendCommand, ['p1=takeoff&p2=0']))

#     mission.readProgress()

#     try:
#         mission.writef(f"<br><br>== Lat: {lat}, Long: {long}, Alt: {alt}, Heading: {heading}")

#         if mission.last_completed <= waypoint_count:
#             mission.writef(drone.waypointCommand(lat, long, 4, heading, True))
#             mission.updateCompleted()
#             waypoint_count += 1

#         mission.writef("<br><br>== All waypoints completed ==")
#     finally:
#         mission.writef("<br><br>== Error was found while performing mission ==")


# mission.run(fullMission)


# End
# #!/usr/bin/python3

# from BaseMission import BaseMission
# import sys
# import math
# import csv

# mission = BaseMission()

# def fullMission():
#     drone = mission.drone
#     mission.writef('<br><br>== Starting Mission ==')
#     mission.writef(mission.timed(drone.sendCommand, ['p1=connect&p2=0']))

#     heading_result, heading_rad = drone.valueCommand('p1=get-heading&p2=0', 'heading')
#     mission.writef(heading_result)
#     heading = math.degrees(heading_rad) % 360

#     fetch_coordinate_csv = f"{globals.userfiles_path}/smartfield_coordinates.csv"
#     with open(fetch_coordinate_csv, 'r') as f:
#         reader = csv.reader(f)
#         coord = next(reader)
#         coord = [float(x) for x in drone]


#     mission.writef('<br><br>== Returning Home Position ==')

#     try:
#         mission.writef(f"<br><br>== Lat: {coord[0]}, Long: {coord[0]}, Alt: 10, Heading: {heading}")

#         if mission.last_completed <= waypoint_count:
#             mission.writef(drone.waypointCommand(coord[0], coord[0], 10, heading, True))
#             mission.updateCompleted()
#             waypoint_count += 1

#         mission.writef("<br><br>== All waypoints completed ==")
#     finally:
#         mission.writef("<br><br>== Error was found while performing mission ==")

#     coord_result, start_coord = drone.coordCommand()
#     mission.writef(f"<br><br>== Landing at coordinates {coord_result} ==")

#     mission.writef('<br><br>== Landing ==')
#     mission.writef(drone.sendCommand('p1=land&p2=0'))
#     mission.baseEnd(takeoff=False,stream=False)

# mission.run(fullMission)
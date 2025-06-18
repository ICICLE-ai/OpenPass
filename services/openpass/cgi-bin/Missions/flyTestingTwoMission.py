# !/usr/bin/python3

from BaseMission import BaseMission
import math
                                                                                                                            
mission = BaseMission()

def fullMission():

    mission.baseStart(stream=False,imagecapture=True)

    drone = mission.drone

    start_coord, current_coordinates = drone.coordCommand()

    heading_result, heading_rad = drone.valueCommand('p1=get-heading&p2=0', 'heading')
    mission.writef(f"{heading_result}")
    heading = math.degrees(heading_rad) % 360

    count = 0
    while count < 3:
        for _ in range(11):
            print("(6, 0, 0)")

        print("(0, 12, 0)")

        for _ in range(11):
            print("(-6, 0, 0)")

        print("(0, 12, 0)")

        count += 1

    for _ in range(11):
        print("(-6, 0, 0)")

    mission.writef("<br><br>== All waypoints completed ==")

    mission.writef("<br><br>== Returning back to the home location ==")
    mission.writef(drone.waypointCommand(current_coordinates[0], current_coordinates[1], 30, heading, True))

    mission.writef('<br><br>== Landing ==')
    mission.writef(drone.sendCommand('p1=land&p2=0'))

    mission.baseEnd(stream=False)

mission.run(fullMission)


#!/usr/bin/python3

from BaseMission import BaseMission
from Helper.LawnmowerFunction import calculate_square_vertices, check_all_points_in_square, create_optimized_flight_route
import Helper.globals as globals
import folium
from datetime import datetime
import time
import threading
 
mission = BaseMission()

keep_capturing = False

def continuous_image_capture():
    while keep_capturing:
        try:
            drone = mission.drone
            mission.writef(mission.timed(drone.sendCommand, ['p1=take-photo&p2=0']))
            mission.writef(mission.timed(drone.sendCommand, ['p1=download&p2=0']))
        except Exception as e:
            mission.writef(f"<br><br>Error capturing image: {str(e)}")
        time.sleep(2)

def fullMission():
    global keep_capturing


    mission.baseStart(stream=False)
    drone = mission.drone
    start_coord, coord_result = drone.coordCommand()
    # coord_result = [39.99263458457224, -83.0088499831398, 5]
    mission.writef(f"{coord_result}")
    if coord_result[0] is 40.0089852740562:
        mission.writef("<br><br> Default Coordinates Identified....")
        mission.writef("<br><br> Abborting....")
        mission.stopf()
    # heading_result, heading_rad = drone.valueCommand('p1=get-heading&p2=0', 'heading')
    # mission.writef(f"{heading_result}")
    # heading = math.degrees(heading_rad) % 360

    mission.writef(f"<br><br> Drone's Current Coordinate: {coord_result}")
    mission.writef(f"<br><br> Chose Square Size: 0.5km.")
    mission.writef(f"<br><br> Drawing Square from Current Coordinate and Heading")

    square_coordinates = calculate_square_vertices(coord_result)
    fetch_coordinate_csv = f"{globals.userfiles_path}/coordinates.csv"

    mission.writef(f"<br><br> Square Coordinates:  <br><br>{square_coordinates}")

    mission.writef(f"<br><br> ========== Checking if the coordinates given are falling under the drone-to-remote covereage area ========== ")

    mission_possibility = check_all_points_in_square(coord_result, fetch_coordinate_csv)

    mission_status = mission_possibility["all_in_square"]
    gps_point_validity = mission_possibility["points"]

    gps_verify_counter = 0
    for row in gps_point_validity:
        lat = float(row[0]) if isinstance(row[0], str) else row[0]
        long = row[1]
        avail = row[2]
        mission.writef(f"<br><br>Path {gps_verify_counter} : Lat {lat}, Long: {long}, Location: {avail}")
        gps_verify_counter = gps_verify_counter + 1

    mission.writef(f"<br><br> ========== Do all of them all under the coverage area: {mission_status} ==========")

    mission.writef(f"<br><br> ========== Calculating and Visualizing Pathway ==========")

    pathway_points = create_optimized_flight_route(coord_result, fetch_coordinate_csv)

    path_counter = 0
    for row in pathway_points:
        lat = float(row[0]) if isinstance(row[0], str) else row[0]
        long = row[1]
        alt = row[2]
        heading = row[3]
        mission.writef(f"<br><br>Path {path_counter} : Lat {lat}, Long: {long}, Alt: {alt}, Head: {heading}")
        path_counter = path_counter + 1

    square_coordinates = calculate_square_vertices(coord_result)

    lats = [coord[0] for coord in square_coordinates]
    lons = [coord[1] for coord in square_coordinates]
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)

    m = folium.Map(location=[center_lat, center_lon])

    for i, coord in enumerate(pathway_points):
        lat, lon, altitude, heading = coord
        popup_text = f"Path Point {i+1}<br>Lat: {lat}<br>Lon: {lon}<br>Altitude: {altitude}<br>Heading: {heading}°"
        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=folium.Icon(icon="arrow-up", prefix="fa", angle=heading, color="green")
        ).add_to(m)

    path_points = [[coord[0], coord[1]] for coord in pathway_points]
    folium.PolyLine(path_points, color="blue", weight=2.5, opacity=1).add_to(m)

    for i, coord in enumerate(square_coordinates):
        lat, lon, altitude, heading = coord
        popup_text = f"Point {i+1}<br>Lat: {lat}<br>Lon: {lon}<br>Altitude: {altitude}<br>Heading: {heading}°"
        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=folium.Icon(icon="arrow-up", prefix="fa", angle=heading)
        ).add_to(m)

    points = [[coord[0], coord[1]] for coord in square_coordinates]
    folium.PolyLine(points + [points[0]], color="red", weight=2.5, opacity=1).add_to(m)

    iframe = m._repr_html_()

    html_content = f"<br><br><div style='width: 600; height: 400;'>{iframe}</div>"

    mission.writef(html_content)

    mission.readProgress()
    
    waypoint_count = 0
    
    capture_thread = threading.Thread(target=continuous_image_capture)
    capture_thread.daemon = True
    
    try:
        keep_capturing = True
        capture_thread.start()
        mission.writef("<br><br>== Started continuous image capture ==")
        
        for coord in pathway_points:
            lat = coord[0]
            lon = coord[1]
            alt = coord[2]
            heading = coord[3]

            mission.writef(f'<br><br>== Waypoint #{waypoint_count+1} ==')
            mission.writef(f"<br><br>== Lat: {lat}, Long: {lon}, Alt: {2}, Heading: {heading}")

            if mission.last_completed <= waypoint_count:
                mission.writef(drone.waypointCommand(lat, lon, 2, heading, True))
                mission.updateCompleted()
                waypoint_count += 1

        mission.writef("<br><br>== All waypoints completed ==")
    finally:
        keep_capturing = False
        capture_thread.join(timeout=5)
        mission.writef("<br><br>== Image capture stopped ==")
    
    mission.writef('<br><br>== Landing ==')
    mission.writef(drone.sendCommand('p1=land&p2=0'))

    mission.baseEnd(stream=False)
    if mission.enableDigitalAgriculture():
        parameters = mission.enableDigitalAgriculture()
        mission.writef(drone.sendCommand(f'p1=sendtotapis&p2=0&p3={parameters[1]}&p4={parameters[2]}&p5={parameters[3]}'))

mission.run(fullMission)
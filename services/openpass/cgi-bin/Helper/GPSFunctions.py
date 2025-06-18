import geopy
import geopy.distance

def drawSquare(start_coord, side_length, heading):
    lat, lon, _ = start_coord

    bot_left_point = geopy.Point(lat, lon)
    bot_right_point = geopy.distance.geodesic(feet=side_length).destination(bot_left_point, heading)
    heading += 90
    top_right_point = geopy.distance.geodesic(feet=side_length).destination(bot_right_point, heading)
    top_left_point = geopy.distance.geodesic(feet=side_length).destination(bot_left_point, heading)

    coordinates = [bot_left_point, bot_right_point, top_right_point, top_left_point]
    return coordinates

if __name__ == "__main__":
    lat = 40.0089852740562
    lon = -83.01683790675908
    alt = 5
    side_length = 200
    heading = 0

    start_coord = [lat, lon, alt]
    coordinates = drawSquare(start_coord, side_length, heading)

    for c in coordinates:
        print(f"Lat: {c[0]}, Lon: {c[1]}")

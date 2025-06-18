import numpy as np
import csv

def calculate_square_vertices(center_coord, csv_path=None, side_length_km=0.1):
    lat, lon, alt = center_coord if len(center_coord) == 3 else [center_coord[0], center_coord[1], 100]
    
    lat_offset = (side_length_km / 2) / 111.0
    lon_offset = (side_length_km / 2) / (111.0 * np.cos(np.radians(lat)))
    
    square_vertices = [
        [lat + lat_offset, lon - lon_offset, alt],
        [lat + lat_offset, lon + lon_offset, alt],
        [lat - lat_offset, lon + lon_offset, alt],
        [lat - lat_offset, lon - lon_offset, alt]
    ]
    
    def calculate_heading(point1, point2):
        lat1, lon1 = point1[0], point1[1]
        lat2, lon2 = point2[0], point2[1]
        
        lat1, lon1 = np.radians(lat1), np.radians(lon1)
        lat2, lon2 = np.radians(lat2), np.radians(lon2)
        
        dlon = lon2 - lon1
        y = np.sin(dlon) * np.cos(lat2)
        x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
        heading = np.degrees(np.arctan2(y, x))
        
        return float((heading + 360) % 360)
    
    mission_waypoints = []
    for i in range(len(square_vertices)):
        next_idx = (i + 1) % len(square_vertices)
        heading = calculate_heading(square_vertices[i], square_vertices[next_idx])
        waypoint = [float(square_vertices[i][0]), float(square_vertices[i][1]), 
                   int(square_vertices[i][2]), float(heading)]
        mission_waypoints.append(waypoint)
    
    return mission_waypoints

def check_all_points_in_square(center_coord, csv_path, side_length_km=0.1):
    lat, lon, alt = center_coord if len(center_coord) == 3 else [center_coord[0], center_coord[1], 100]
    
    lat_offset = (side_length_km / 2) / 111.0
    lon_offset = (side_length_km / 2) / (111.0 * np.cos(np.radians(lat)))
    
    def is_point_in_square(point):
        p_lat, p_lon = point[0], point[1]
        return (lat - lat_offset <= p_lat <= lat + lat_offset and
                lon - lon_offset <= p_lon <= lon + lon_offset)
    
    csv_points = []
    points_status = []
    
    try:
        with open(csv_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) >= 2:
                    try:
                        p_lat = float(row[0])
                        p_lon = float(row[1])
                        point = [p_lat, p_lon, alt]
                        csv_points.append(point)
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return {'all_in_square': False, 'points': []}
    
    csv_points.sort(key=lambda p: -p[0])
    
    csv_points_with_status = []
    for point in csv_points:
        is_in_square = is_point_in_square(point)
        points_status.append(is_in_square)
        csv_points_with_status.append([float(point[0]), float(point[1]), "Inside" if is_in_square else "Outside"])
    
    all_in_square = bool(all(points_status))
    
    return {
        'all_in_square': all_in_square,
        'points': csv_points_with_status
    }

def create_optimized_flight_route(center_coord, csv_path, side_length_km=0.1):
    lat, lon, alt = center_coord if len(center_coord) == 3 else [center_coord[0], center_coord[1], 100]
    
    lat_offset = (side_length_km / 2) / 111.0
    lon_offset = (side_length_km / 2) / (111.0 * np.cos(np.radians(lat)))
    
    def is_point_in_square(point):
        p_lat, p_lon = point[0], point[1]
        return (lat - lat_offset <= p_lat <= lat + lat_offset and
                lon - lon_offset <= p_lon <= lon + lon_offset)
    
    def calculate_heading(point1, point2):
        lat1, lon1 = point1[0], point1[1]
        lat2, lon2 = point2[0], point2[1]
        
        lat1, lon1 = np.radians(lat1), np.radians(lon1)
        lat2, lon2 = np.radians(lat2), np.radians(lon2)
        
        dlon = lon2 - lon1
        y = np.sin(dlon) * np.cos(lat2)
        x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
        heading = np.degrees(np.arctan2(y, x))
        
        return float((heading + 360) % 360)
    
    csv_points = []
    
    try:
        with open(csv_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) >= 2:
                    try:
                        p_lat = float(row[0])
                        p_lon = float(row[1])
                        point = [p_lat, p_lon, alt]
                        csv_points.append(point)
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return [[float(lat), float(lon), int(alt), 0.0]]
    
    csv_points.sort(key=lambda p: -p[0])
    
    valid_points = []
    for point in csv_points:
        if is_point_in_square(point):
            valid_points.append(point)
    
    valid_points_with_heading = []
    for i in range(len(valid_points)):
        next_idx = (i + 1) % len(valid_points) if i < len(valid_points) - 1 else 0
        heading = calculate_heading(valid_points[i], valid_points[next_idx])
        point_with_heading = valid_points[i] + [heading]
        valid_points_with_heading.append(point_with_heading)
    
    optimized_route = [[float(lat), float(lon), int(alt), 0.0]]  # Start at center
    
    for point in valid_points_with_heading:
        optimized_route.append([float(point[0]), float(point[1]), int(point[2]), float(point[3])])
    
    optimized_route.append([float(lat), float(lon), int(alt) , 0.0])
    
    for i in range(len(optimized_route) - 1):
        next_point = optimized_route[i + 1]
        optimized_route[i][3] = calculate_heading(
            [optimized_route[i][0], optimized_route[i][1]],
            [next_point[0], next_point[1]]
        )
    
    return optimized_route

# if __name__ == "__main__":
#     center = [40.008242180294445, -83.01631842045622, 100]
#     csv_filename = "/home/icicle/Developer/devel/openpasswebsite.git/coordinates.csv"
    
#     square_vertices = calculate_square_vertices(center)
#     points_info = check_all_points_in_square(center, csv_filename)
#     optimized_route = create_optimized_flight_route(center, csv_filename)
    
#     result = {
#         'current_coordinate': [float(center[0]), float(center[1]), int(center[2])],
#         'square_vertices': square_vertices,
#         'csv_points': points_info['points'],
#         'all_points_in_square': points_info['all_in_square'],
#         'optimized_route': optimized_route
#     }
    
#     print(result)
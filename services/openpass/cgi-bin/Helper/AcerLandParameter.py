import math
import csv
from io import StringIO
import folium
from folium import plugins

def get_waypoints(current_coordinate, side, flight_height=20, overlap_forward=80, overlap_side=60, 
                 ground_coverage_width=30, photo_interval_time=2, field_width=63.6, field_height=63.6):
    """
    Generate waypoints for orthomosaic drone flight over a 1-acre field.
    
    Parameters:
    current_coordinate: [lat, lon] coordinates of one corner
    side: "A", "B", "C", or "D" - which corner the current_coordinate represents
        A = (0,0) - bottom left
        B = (1,0) - bottom right  
        C = (1,1) - top right
        D = (0,1) - top left
    flight_height: Height above ground in meters (default: 20m)
    overlap_forward: Forward overlap percentage (default: 80%)
    overlap_side: Side overlap percentage (default: 60%)
    ground_coverage_width: Camera ground coverage width at flight height (default: 30m)
    photo_interval_time: Time between photos in seconds (default: 2s)
    field_width: Field width in meters (default: 63.6m for 1 acre square)
    field_height: Field height in meters (default: 63.6m for 1 acre square)
    
    Returns:
    Tuple containing:
    - List of waypoint coordinates [lat, lon, alt] 
    - CSV string with flight plan data
    - Folium map object with satellite view and interactive features
    """
    
    def meters_to_lat_lon(lat, lon, dx_meters, dy_meters):
        """Convert meter offsets to lat/lon offsets"""
        # 1 degree latitude ≈ 111,320 meters
        # 1 degree longitude ≈ 111,320 * cos(latitude) meters
        lat_offset = dy_meters / 111320.0
        lon_offset = dx_meters / (111320.0 * math.cos(math.radians(lat)))
        return lat + lat_offset, lon + lon_offset
    
    # Calculate all four corners based on the given corner and side
    lat, lon = current_coordinate
    
    if side.upper() == "A":  # Bottom left (0,0)
        A = [lat, lon]
        B_lat, B_lon = meters_to_lat_lon(lat, lon, field_width, 0)
        B = [B_lat, B_lon]
        C_lat, C_lon = meters_to_lat_lon(lat, lon, field_width, field_height)
        C = [C_lat, C_lon]
        D_lat, D_lon = meters_to_lat_lon(lat, lon, 0, field_height)
        D = [D_lat, D_lon]
        
    elif side.upper() == "B":  # Bottom right (1,0)
        B = [lat, lon]
        A_lat, A_lon = meters_to_lat_lon(lat, lon, -field_width, 0)
        A = [A_lat, A_lon]
        C_lat, C_lon = meters_to_lat_lon(lat, lon, 0, field_height)
        C = [C_lat, C_lon]
        D_lat, D_lon = meters_to_lat_lon(lat, lon, -field_width, field_height)
        D = [D_lat, D_lon]
        
    elif side.upper() == "C":  # Top right (1,1)
        C = [lat, lon]
        A_lat, A_lon = meters_to_lat_lon(lat, lon, -field_width, -field_height)
        A = [A_lat, A_lon]
        B_lat, B_lon = meters_to_lat_lon(lat, lon, 0, -field_height)
        B = [B_lat, B_lon]
        D_lat, D_lon = meters_to_lat_lon(lat, lon, -field_width, 0)
        D = [D_lat, D_lon]
        
    elif side.upper() == "D":  # Top left (0,1)
        D = [lat, lon]
        A_lat, A_lon = meters_to_lat_lon(lat, lon, 0, -field_height)
        A = [A_lat, A_lon]
        B_lat, B_lon = meters_to_lat_lon(lat, lon, field_width, -field_height)
        B = [B_lat, B_lon]
        C_lat, C_lon = meters_to_lat_lon(lat, lon, field_width, 0)
        C = [C_lat, C_lon]
        
    else:
        raise ValueError("Side must be 'A', 'B', 'C', or 'D'")
    
    print(f"Calculated field corners:")
    print(f"A (bottom-left): [{A[0]:.8f}, {A[1]:.8f}]")
    print(f"B (bottom-right): [{B[0]:.8f}, {B[1]:.8f}]") 
    print(f"C (top-right): [{C[0]:.8f}, {C[1]:.8f}]")
    print(f"D (top-left): [{D[0]:.8f}, {D[1]:.8f}]")
    
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two lat/lon points in meters"""
        R = 6371000  # Earth radius in meters
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        
        a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    def interpolate_coordinates(coord1, coord2, fraction):
        """Interpolate between two coordinates"""
        lat = coord1[0] + (coord2[0] - coord1[0]) * fraction
        lon = coord1[1] + (coord2[1] - coord1[1]) * fraction
        return [lat, lon]
    
    # Use the specified field dimensions
    width_meters = field_width
    height_meters = field_height
    
    # Calculate flight line spacing based on overlap requirements
    line_spacing = ground_coverage_width * (1 - overlap_side/100)
    photo_spacing = ground_coverage_width * (1 - overlap_forward/100)
    
    # Calculate number of flight lines and photos per line
    num_lines = max(1, int(math.ceil(width_meters / line_spacing)) + 1)
    photos_per_line = max(1, int(math.ceil(height_meters / photo_spacing)) + 1)
    
    waypoints = []
    
    # Generate flight pattern (lawnmower/boustrophedon pattern)
    for line_idx in range(num_lines):
        # Calculate position along width (A-B direction)
        width_fraction = line_idx / max(1, num_lines - 1) if num_lines > 1 else 0
        width_fraction = min(1.0, width_fraction)
        
        # Determine if this is an odd or even line (for alternating direction)
        reverse_direction = line_idx % 2 == 1
        
        for photo_idx in range(photos_per_line):
            # Calculate position along height (A-D direction)
            if reverse_direction:
                height_fraction = 1 - (photo_idx / max(1, photos_per_line - 1))
            else:
                height_fraction = photo_idx / max(1, photos_per_line - 1) if photos_per_line > 1 else 0
            
            height_fraction = max(0.0, min(1.0, height_fraction))
            
            # Calculate the actual coordinates using bilinear interpolation
            # Bottom edge: interpolate between A and B
            bottom_point = interpolate_coordinates(A, B, width_fraction)
            # Top edge: interpolate between D and C  
            top_point = interpolate_coordinates(D, C, width_fraction)
            # Final point: interpolate between bottom and top
            waypoint = interpolate_coordinates(bottom_point, top_point, height_fraction)
            
            # Add altitude (height above ground)
            waypoint.append(flight_height)
            waypoints.append(waypoint)
    
    # Generate CSV content
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    
    # Write header
    csv_writer.writerow(['Waypoint', 'Latitude', 'Longitude', 'Altitude_AGL_m', 
                        'Action', 'Photo_Interval_s'])
    
    # Write waypoints
    for i, wp in enumerate(waypoints):
        csv_writer.writerow([
            f'WP{i+1:03d}', 
            f'{wp[0]:.8f}', 
            f'{wp[1]:.8f}', 
            wp[2],
            'PHOTO' if i % int(photo_interval_time) == 0 else 'WAYPOINT',
            photo_interval_time if i % int(photo_interval_time) == 0 else ''
        ])
    
    csv_content = csv_buffer.getvalue()
    
    # Create interactive folium map with satellite view
    # Calculate center of the field
    center_lat = (A[0] + B[0] + C[0] + D[0]) / 4
    center_lon = (A[1] + B[1] + C[1] + D[1]) / 4
    
    # Create map with satellite imagery
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=18,
        tiles=None
    )
    
    # Add satellite imagery
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add OpenStreetMap as alternative
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='Street Map',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Define colors for different elements
    corner_colors = {'A': 'red', 'B': 'blue', 'C': 'green', 'D': 'orange'}
    
    # Add corner markers
    corners = {'A': A, 'B': B, 'C': C, 'D': D}
    corner_names = {
        'A': 'A - Bottom Left (0,0)',
        'B': 'B - Bottom Right (1,0)', 
        'C': 'C - Top Right (1,1)',
        'D': 'D - Top Left (0,1)'
    }
    
    for corner_id, coord in corners.items():
        folium.Marker(
            location=[coord[0], coord[1]],
            popup=f"<b>Corner {corner_id}</b><br>{corner_names[corner_id]}<br>Lat: {coord[0]:.8f}<br>Lon: {coord[1]:.8f}",
            tooltip=f"Corner {corner_id}",
            icon=folium.Icon(color=corner_colors[corner_id], icon='info-sign', prefix='glyphicon')
        ).add_to(m)
    
    # Add field boundary
    field_boundary = [A, B, C, D, A]  # Close the polygon
    folium.PolyLine(
        locations=field_boundary,
        color='red',
        weight=3,
        opacity=0.8,
        popup="Field Boundary (1 acre)"
    ).add_to(m)
    
    # Add waypoint markers and flight path
    flight_path = []
    waypoint_group = folium.FeatureGroup(name="Waypoints").add_to(m)
    
    for i, wp in enumerate(waypoints):
        lat, lon, alt = wp
        flight_path.append([lat, lon])
        
        # Create popup content with CSV data
        popup_content = f"""
        <div style='width: 200px'>
            <b>Waypoint {i+1:03d}</b><br>
            <b>Latitude:</b> {lat:.8f}<br>
            <b>Longitude:</b> {lon:.8f}<br>
            <b>Altitude AGL:</b> {alt}m<br>
            <b>Action:</b> {'PHOTO' if i % int(photo_interval_time) == 0 else 'WAYPOINT'}<br>
            <b>Sequence:</b> {i+1} of {len(waypoints)}
        </div>
        """
        
        # Different icons for photo vs waypoint
        if i % int(photo_interval_time) == 0:
            icon = folium.Icon(color='darkgreen', icon='camera', prefix='glyphicon')
            tooltip_text = f"Photo Point {i+1}"
        else:
            icon = folium.Icon(color='lightblue', icon='record', prefix='glyphicon')
            tooltip_text = f"Waypoint {i+1}"
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_content, max_width=250),
            tooltip=tooltip_text,
            icon=icon
        ).add_to(waypoint_group)
    
    # Add flight path
    if len(flight_path) > 1:
        folium.PolyLine(
            locations=flight_path,
            color='blue',
            weight=2,
            opacity=0.7,
            popup="Drone Flight Path"
        ).add_to(m)
        
        # Add arrow markers to show direction
        for i in range(0, len(flight_path)-1, max(1, len(flight_path)//10)):
            if i < len(flight_path) - 1:
                folium.plugins.PolyLineTextPath(
                    folium.PolyLine(
                        locations=[flight_path[i], flight_path[i+1]],
                        weight=0
                    ),
                    text="→",
                    repeat=False,
                    offset=7,
                    attributes={'fill': 'blue', 'font-weight': 'bold', 'font-size': '14'}
                ).add_to(m)
    
    # Add CSV data as a separate layer
    csv_html = f"""
    <div style='position: fixed; 
                top: 10px; right: 10px; width: 300px; height: 200px; 
                background-color: white; border: 2px solid grey; z-index:9999; 
                font-size: 10px; overflow-y: scroll; padding: 10px'>
    <h4>Flight Plan CSV Data</h4>
    <pre>{csv_content[:500]}{'...' if len(csv_content) > 500 else ''}</pre>
    <button onclick="downloadCSV()">Download Full CSV</button>
    </div>
    
    <script>
    function downloadCSV() {{
        var csv = `{csv_content}`;
        var blob = new Blob([csv], {{type: 'text/csv'}});
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.setAttribute('hidden', '');
        a.setAttribute('href', url);
        a.setAttribute('download', 'drone_waypoints.csv');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }}
    </script>
    """
    
    m.get_root().html.add_child(folium.Element(csv_html))
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add measurement plugin
    plugins.MeasureControl().add_to(m)
    
    # Add fullscreen button
    plugins.Fullscreen().add_to(m)
    
    # Add legend
    legend_html = f"""
    <div style='position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 150px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size: 12px; padding: 10px'>
    <p><b>Legend</b></p>
    <p><i class="fa fa-circle" style="color:red"></i> Corner A (Given: {side})</p>
    <p><i class="fa fa-camera" style="color:green"></i> Photo Points</p>
    <p><i class="fa fa-circle" style="color:blue"></i> Navigation Points</p>
    <p><i style="color:blue">→</i> Flight Direction</p>
    <p><b>Total Distance:</b> {len(waypoints) * photo_spacing:.0f}m</p>
    </div>
    """
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Print summary information
    print(f"\nInput: Corner {side.upper()} at [{current_coordinate[0]:.8f}, {current_coordinate[1]:.8f}]")
    print(f"Field Dimensions: {width_meters:.1f}m x {height_meters:.1f}m ({width_meters * height_meters:.0f} sq meters)")
    print(f"Flight Lines: {num_lines}")
    print(f"Photos per Line: {photos_per_line}")
    print(f"Total Waypoints: {len(waypoints)}")
    print(f"Estimated Flight Time: {len(waypoints) * photo_interval_time / 60:.1f} minutes")
    print(f"Line Spacing: {line_spacing:.1f}m")
    print(f"Photo Spacing: {photo_spacing:.1f}m")
    print(f"Map created with satellite view and interactive features")
    print("\nCSV Content Preview:")
    print(csv_content[:300] + "..." if len(csv_content) > 300 else csv_content)
    
    return waypoints, csv_content, m, line_spacing, photo_spacing, photo_interval_time, photos_per_line, num_lines, width_meters, height_meters

# Example usage:
if __name__ == "__main__":
    # Example: Give one corner coordinate and specify which corner it is
    current_coordinate = [40.008002333334815, -83.0186213333282]  # Your known corner
    side = "A"  # This coordinate represents corner A (bottom-left)
    
    waypoints, csv_content, m, line_spacing, photo_spacing, photo_interval_time, photos_per_line, num_lines, width_meters, height_meters = get_waypoints(current_coordinate, side)
    
    # Save the map
    m.save('drone_flight_plan.html')
    print(f"\nInteractive map saved as 'drone_flight_plan.html'")
    print("Open this file in your browser to view the satellite map with flight path!")
    
    # Save CSV file
    with open('drone_waypoints.csv', 'w', newline='') as f:
        f.write(csv_content)
    print("CSV file saved as 'drone_waypoints.csv'")
    
    # Alternative examples:
    # waypoints, csv_data, map_obj = get_waypoints([40.123456, -74.123456], "B")  # Bottom-right
    # waypoints, csv_data, map_obj = get_waypoints([40.123456, -74.123456], "C")  # Top-right  
    # waypoints, csv_data, map_obj = get_waypoints([40.123456, -74.123456], "D")  # Top-left
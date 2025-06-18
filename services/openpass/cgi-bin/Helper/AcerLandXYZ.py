import math
import csv
from io import StringIO
import folium
from folium import plugins

def get_waypoints_xyz(start_gps_coordinate, start_corner="A", flight_height_z=20, 
                     photo_spacing_x=6, line_spacing_y=12, field_width=63.6, field_height=63.6):
    """
    Generate waypoints for orthomosaic drone flight using relative XYZ coordinates.
    
    CONSTANT VALUES FOR 1-ACRE FIELD:
    ================================
    X-axis: 6m forward movement between photos (80% overlap)
    Y-axis: 12m sideways movement between flight lines (60% overlap)  
    Z-axis: 20m altitude above ground level (constant)
    
    FLIGHT PATTERN:
    ==============
    - Photos every 6m forward (X-direction)
    - New flight line every 12m sideways (Y-direction)
    - 11 photos per line, 6 flight lines total
    - Alternating directions (lawnmower pattern)
    
    Parameters:
    start_gps_coordinate: [lat, lon] - Starting GPS position
    start_corner: "A", "B", "C", or "D" - Which corner to start from
    flight_height_z: Z-axis constant (altitude in meters)
    photo_spacing_x: X-axis constant (forward spacing in meters)
    line_spacing_y: Y-axis constant (sideways spacing in meters)
    field_width: Field width in meters
    field_height: Field height in meters
    
    Returns:
    Tuple containing:
    - List of waypoints with XYZ coordinates [x, y, z, lat, lon]
    - CSV string with flight plan
    - Folium map object
    - Flight statistics dictionary
    """
    
    def meters_to_lat_lon(lat, lon, dx_meters, dy_meters):
        """Convert XY meter offsets to lat/lon offsets"""
        lat_offset = dy_meters / 111320.0
        lon_offset = dx_meters / (111320.0 * math.cos(math.radians(lat)))
        return lat + lat_offset, lon + lon_offset
    
    # Calculate constant values
    photos_per_line = int(field_height / photo_spacing_x) + 1
    num_flight_lines = int(field_width / line_spacing_y) + 1
    
    # Starting GPS coordinates
    start_lat, start_lon = start_gps_coordinate
    
    # Calculate field corners in XYZ coordinates based on starting corner
    if start_corner.upper() == "A":  # Bottom-left (0,0,Z)
        corner_offsets = {
            'A': (0, 0), 'B': (field_width, 0), 
            'C': (field_width, field_height), 'D': (0, field_height)
        }
        origin_x, origin_y = 0, 0
    elif start_corner.upper() == "B":  # Bottom-right (W,0,Z)
        corner_offsets = {
            'A': (-field_width, 0), 'B': (0, 0),
            'C': (0, field_height), 'D': (-field_width, field_height)
        }
        origin_x, origin_y = field_width, 0
    elif start_corner.upper() == "C":  # Top-right (W,H,Z)
        corner_offsets = {
            'A': (-field_width, -field_height), 'B': (0, -field_height),
            'C': (0, 0), 'D': (-field_width, 0)
        }
        origin_x, origin_y = field_width, field_height
    elif start_corner.upper() == "D":  # Top-left (0,H,Z)
        corner_offsets = {
            'A': (0, -field_height), 'B': (field_width, -field_height),
            'C': (field_width, 0), 'D': (0, 0)
        }
        origin_x, origin_y = 0, field_height
    else:
        raise ValueError("start_corner must be 'A', 'B', 'C', or 'D'")
    
    # Generate XYZ waypoints
    waypoints = []
    movement_count = 0
    total_photos = 0
    
    print(f"🚁 DRONE FLIGHT CONSTANTS FOR 1-ACRE FIELD:")
    print(f"📐 X-axis movement: {photo_spacing_x}m forward (between photos)")
    print(f"📐 Y-axis movement: {line_spacing_y}m sideways (between flight lines)")
    print(f"📐 Z-axis altitude: {flight_height_z}m above ground (constant)")
    print(f"📊 Photos per line: {photos_per_line}")
    print(f"📊 Number of flight lines: {num_flight_lines}")
    print(f"🔄 Direction changes: Every {photos_per_line} movements")
    print(f"📍 Starting corner: {start_corner} at GPS {start_gps_coordinate}")
    print("=" * 60)
    
    for line_idx in range(num_flight_lines):
        # Calculate Y position (sideways movement)
        y_pos = line_idx * line_spacing_y
        
        # Determine flight direction (alternating for lawnmower pattern)
        reverse_direction = line_idx % 2 == 1
        
        print(f"✈️  FLIGHT LINE {line_idx + 1}:")
        print(f"   Y-position: {y_pos}m from origin")
        print(f"   Direction: {'BACKWARD' if reverse_direction else 'FORWARD'}")
        
        for photo_idx in range(photos_per_line):
            # Calculate X position (forward movement)
            if reverse_direction:
                x_pos = (photos_per_line - 1 - photo_idx) * photo_spacing_x
            else:
                x_pos = photo_idx * photo_spacing_x
            
            # XYZ coordinates relative to field origin
            x_field = x_pos
            y_field = y_pos
            z_field = flight_height_z
            
            # Convert to GPS coordinates
            gps_lat, gps_lon = meters_to_lat_lon(start_lat, start_lon, x_field, y_field)
            
            # Store waypoint with both XYZ and GPS
            waypoint = {
                'x': x_field,
                'y': y_field, 
                'z': z_field,
                'lat': gps_lat,
                'lon': gps_lon,
                'line': line_idx + 1,
                'photo_in_line': photo_idx + 1,
                'action': 'PHOTO'
            }
            waypoints.append(waypoint)
            movement_count += 1
            total_photos += 1
            
            print(f"   📷 Photo {photo_idx + 1}: X={x_field}m, Y={y_field}m, Z={z_field}m")
        
        print(f"   ✅ Line completed: {photos_per_line} photos taken")
        if line_idx < num_flight_lines - 1:
            print(f"   ➡️  Moving {line_spacing_y}m sideways to next line...")
        print()
    
    # Generate CSV content
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    
    # Write header
    csv_writer.writerow(['Waypoint', 'X_meters', 'Y_meters', 'Z_meters', 'Latitude', 'Longitude', 
                        'Action', 'Flight_Line', 'Photo_In_Line'])
    
    # Write waypoints
    for i, wp in enumerate(waypoints):
        csv_writer.writerow([
            f'WP{i+1:03d}',
            f'{wp["x"]:.1f}',
            f'{wp["y"]:.1f}', 
            f'{wp["z"]:.1f}',
            f'{wp["lat"]:.8f}',
            f'{wp["lon"]:.8f}',
            wp['action'],
            wp['line'],
            wp['photo_in_line']
        ])
    
    csv_content = csv_buffer.getvalue()
    
    # Create folium map
    m = folium.Map(
        location=[start_lat, start_lon],
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
    
    # Add field corners
    corners_gps = {}
    for corner_id, (x_offset, y_offset) in corner_offsets.items():
        corner_lat, corner_lon = meters_to_lat_lon(start_lat, start_lon, x_offset, y_offset)
        corners_gps[corner_id] = [corner_lat, corner_lon]
    
    corner_colors = {'A': 'red', 'B': 'blue', 'C': 'green', 'D': 'orange'}
    corner_names = {
        'A': 'A - Bottom Left (0,0)',
        'B': 'B - Bottom Right (W,0)', 
        'C': 'C - Top Right (W,H)',
        'D': 'D - Top Left (0,H)'
    }
    
    for corner_id, coord in corners_gps.items():
        is_start = corner_id == start_corner.upper()
        folium.Marker(
            location=coord,
            popup=f"<b>Corner {corner_id}</b><br>{corner_names[corner_id]}<br>{'START POINT' if is_start else ''}<br>GPS: {coord[0]:.8f}, {coord[1]:.8f}",
            tooltip=f"Corner {corner_id} {'(START)' if is_start else ''}",
            icon=folium.Icon(
                color=corner_colors[corner_id], 
                icon='play' if is_start else 'info-sign', 
                prefix='glyphicon'
            )
        ).add_to(m)
    
    # Add field boundary
    boundary_coords = [corners_gps['A'], corners_gps['B'], corners_gps['C'], corners_gps['D'], corners_gps['A']]
    folium.PolyLine(
        locations=boundary_coords,
        color='red',
        weight=3,
        opacity=0.8,
        popup="1-Acre Field Boundary"
    ).add_to(m)
    
    # Add waypoints and flight path
    flight_path = []
    line_colors = ['blue', 'green', 'purple', 'orange', 'darkred', 'darkblue']
    
    for i, wp in enumerate(waypoints):
        flight_path.append([wp['lat'], wp['lon']])
        
        # Color code by flight line
        line_color = line_colors[(wp['line'] - 1) % len(line_colors)]
        
        popup_content = f"""
        <div style='width: 250px'>
            <b>Waypoint {i+1:03d}</b><br>
            <b>XYZ Position:</b> ({wp['x']:.1f}m, {wp['y']:.1f}m, {wp['z']}m)<br>
            <b>GPS:</b> {wp['lat']:.8f}, {wp['lon']:.8f}<br>
            <b>Flight Line:</b> {wp['line']}<br>
            <b>Photo:</b> {wp['photo_in_line']} of {photos_per_line}<br>
            <b>Action:</b> {wp['action']}
        </div>
        """
        
        folium.Marker(
            location=[wp['lat'], wp['lon']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"WP{i+1:03d} - Line {wp['line']}",
            icon=folium.Icon(color='darkgreen', icon='camera', prefix='glyphicon')
        ).add_to(m)
    
    # Add flight path lines
    current_line = 1
    line_points = []
    
    for wp in waypoints:
        if wp['line'] == current_line:
            line_points.append([wp['lat'], wp['lon']])
        else:
            # Draw completed line
            if len(line_points) > 1:
                line_color = line_colors[(current_line - 1) % len(line_colors)]
                folium.PolyLine(
                    locations=line_points,
                    color=line_color,
                    weight=3,
                    opacity=0.8,
                    popup=f"Flight Line {current_line}"
                ).add_to(m)
            
            # Start new line
            current_line = wp['line']
            line_points = [[wp['lat'], wp['lon']]]
    
    # Draw final line
    if len(line_points) > 1:
        line_color = line_colors[(current_line - 1) % len(line_colors)]
        folium.PolyLine(
            locations=line_points,
            color=line_color,
            weight=3,
            opacity=0.8,
            popup=f"Flight Line {current_line}"
        ).add_to(m)
    
    # Add CSV data panel
    csv_html = f"""
    <div style='position: fixed; 
                top: 10px; right: 10px; width: 350px; height: 250px; 
                background-color: white; border: 2px solid grey; z-index:9999; 
                font-size: 10px; overflow-y: scroll; padding: 10px'>
    <h4>XYZ Flight Plan Data</h4>
    <p><b>Constants:</b> X={photo_spacing_x}m, Y={line_spacing_y}m, Z={flight_height_z}m</p>
    <pre>{csv_content[:400]}{'...' if len(csv_content) > 400 else ''}</pre>
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
        a.setAttribute('download', 'drone_xyz_waypoints.csv');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }}
    </script>
    """
    
    m.get_root().html.add_child(folium.Element(csv_html))
    
    # Add legend
    legend_html = f"""
    <div style='position: fixed; 
                bottom: 50px; left: 50px; width: 250px; height: 200px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size: 12px; padding: 10px'>
    <p><b>XYZ Flight Constants</b></p>
    <p><b>X-axis:</b> {photo_spacing_x}m forward steps</p>
    <p><b>Y-axis:</b> {line_spacing_y}m sideways steps</p>
    <p><b>Z-axis:</b> {flight_height_z}m altitude (constant)</p>
    <p><b>Photos per line:</b> {photos_per_line}</p>
    <p><b>Turn frequency:</b> Every {photos_per_line} movements</p>
    <p><b>Total photos:</b> {total_photos}</p>
    <p><b>Flight pattern:</b> Lawnmower (alternating)</p>
    </div>
    """
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add layer control and plugins
    folium.LayerControl().add_to(m)
    plugins.MeasureControl().add_to(m)
    plugins.Fullscreen().add_to(m)
    
    # Flight statistics
    stats = {
        'total_waypoints': len(waypoints),
        'total_photos': total_photos,
        'flight_lines': num_flight_lines,
        'photos_per_line': photos_per_line,
        'x_spacing': photo_spacing_x,
        'y_spacing': line_spacing_y,
        'z_altitude': flight_height_z,
        'movements_per_turn': photos_per_line,
        'field_coverage': f"{field_width}m x {field_height}m"
    }
    
    print(f"📈 FLIGHT SUMMARY:")
    print(f"   Total waypoints: {stats['total_waypoints']}")
    print(f"   Total photos: {stats['total_photos']}")
    print(f"   Movement pattern: {photos_per_line} forward → turn → {line_spacing_y}m sideways → repeat")
    print(f"   Estimated flight time: {stats['total_waypoints'] * 2 / 60:.1f} minutes")
    
    return waypoints, csv_content, m, stats

# Example usage:
if __name__ == "__main__":
    # Start from any GPS coordinate - the function will create relative XYZ pattern
    start_gps = [40.008002333334815, -83.0186213333282]  # Any GPS location
    start_corner = "A"  # Which corner this GPS represents
    
    waypoints, csv_data, map_obj, statistics = get_waypoints_xyz(start_gps, start_corner)
    
    # Save files
    map_obj.save('drone_xyz_flight_plan.html')
    with open('drone_xyz_waypoints.csv', 'w', newline='') as f:
        f.write(csv_data)
    
    print(f"\n🗺️  Map saved: drone_xyz_flight_plan.html")
    print(f"📄 CSV saved: drone_xyz_waypoints.csv")
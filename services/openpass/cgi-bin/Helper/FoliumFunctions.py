import folium
from folium.plugins import HeatMap

def createHeatMap(df, key):
  # Create Map
  heat_map = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=20)
  # Prepare the data for the heatmap
  heat_data = [[row['lat'], row['lon'], row[key]] for index, row in df.iterrows()]
  # Add the heatmap layer
  HeatMap(heat_data, radius=15).add_to(heat_map)
  # Save heat map
  heat_map.save("/opt/bitnami/apache/htdocs/gps_waypoints_map.html")

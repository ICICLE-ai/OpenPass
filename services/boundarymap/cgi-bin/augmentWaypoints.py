"""
Goal:
    - Loop through each line of waypoint data
    - If line is waypoint, calculate x,y,z,angle data using lat,long,alt,heading
    - Add that data back to line and write line to user-augmented-waypoints.csv

/opt/bitnami/apache2/htdocs/userfiles/user-waypoints.csv

"""
import math

waypoints_file = open("/opt/bitnami/apache2/htdocs/userfiles/user-waypoints.csv","r").readlines()
augmented_file = open("/opt/bitnami/apache2/htdocs/userfiles/user-augmented-waypoints.csv","w")


def is_waypoint(line):
    waypoints = line.split(",")

    try:
        float(waypoints[0])
        return True
    except ValueError:
        return False

def augment_waypoint(stack):
    
    # Split previous and current waypoints into arrays
    prev_line = stack[0].split(",")
    curr_line = stack[1].split(",")

    # Get latitude, longitude, altitude, and heading from both
    prev_lat,prev_long,prev_alt,prev_head=float(prev_line[0]),float(prev_line[1]),float(prev_line[2]),float(prev_line[3])
    curr_lat,curr_long,curr_alt,curr_head=float(curr_line[0]),float(curr_line[1]),float(curr_line[2]),float(curr_line[3])
    

    # Calculate x,y,z, and heading
    EARTH_CIRCUM_IN_M = 6371000
    PI = math.pi
    CONVERSION_TO_FEET = 3.281

    x = (EARTH_CIRCUM_IN_M * ((curr_lat-prev_lat) * (PI/180))) * CONVERSION_TO_FEET
    y = (EARTH_CIRCUM_IN_M * math.cos(x) * ((curr_long-prev_long) * (PI/180))) * CONVERSION_TO_FEET
    z = curr_alt-prev_alt
    heading = curr_head-prev_head

    # Join all strings into one waypoint
    curr_line.pop() # remove "\n
    curr_line = ','.join(curr_line)
    augmented_waypoint = ','.join([curr_line,str(x),str(y),str(z),str(heading)])
    augmented_waypoint += '"\n'

    return augmented_waypoint

def augment_header(line):
    
    # Remove "\n
    header = line.split(",")
    header.pop()
    header = ','.join(header)

    # Add additional headers and "\n
    augmented_header = ','.join([header,"x","y","z","heading"])
    augmented_header += '"\n'

    return augmented_header

# Stack to hold prev and curr waypoints
stack = []

# Loop through lines in user-waypoints.csv
for index,line in enumerate(waypoints_file):
    # Alter header
    if index == 0:
        line = augment_header(line)
    # Check for waypoint
    if is_waypoint(line):
        stack.append(line)
        # Augment current waypoint using current and previouslines
        if len(stack) == 2:
            line = augment_waypoint(stack)
            stack.pop(0)

    # Write line to user-augmented-waypoints.csv
    augmented_file.write(line)


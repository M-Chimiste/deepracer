import math

# Constants
SPEED_THRESHOLD = 6
STEERING_THRESHOLD = 15
TOTAL_STEPS = 85
DIRECTION_THRESHOLD = 15.0

# End Constants

def reward_function(params):
# --------- Start Params ---------
    all_wheels_on_track = params['all_wheels_on_track'] # bool

    track_width = params['track_width']
    
    distance_from_center = params['distance_from_center']

    waypoints = params['waypoints']

    closest_waypoint = params['closest_waypoints']
    
    current_waypoint = waypoints[closest_waypoint[0]]
    next_waypoint = waypoints[closest_waypoint[1]]


    wheel_direction = params['steering_angle']

    car_direction = ['heading']

    steering = abs(params['steering_angle'])

    speed = params['speed']

    track_progress = params ['progress']

    reward = 1  # initial reward
    punishment = 1 # used to penalize

# --------- End Params ---------

    # Give a big reward if you finished the track!
    if track_progress == 100:
        reward = reward + 150
    # Sanity Check 
    if reward < 0:
        reward = 0
    
    #Make sure direction of car is that of track
    track_heading = math.atan2(next_waypoint[1] - current_waypoint[1], next_waypoint[0] - current_waypoint[0])
    track_heading = math.degrees(track_heading)
    #Compare correct direction V direction of car
    heading_delta = abs(track_heading - car_direction)

    if heading_delta > DIRECTION_THRESHOLD:
        punishment= 1-(heading_delta/20)

        if punishment < 0 or punishment > 1:
            punishment = 0
        
        reward = reward * punishment


    if speed < SPEED_THRESHOLD:
        reward = reward * 0.8

    if steering > STEERING_THRESHOLD:
        reward = reward * 0.7
    
    if track_progress == 100:
        reward = reward + 100
    
    if not (all_wheels_on_track):
        reward = 0
    
    return float(reward)

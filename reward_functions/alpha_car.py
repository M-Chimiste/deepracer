"""
{
    "all_wheels_on_track": Boolean,        # flag to indicate if the agent is on the track
    "x": float,                            # agent's x-coordinate in meters
    "y": float,                            # agent's y-coordinate in meters
    "closest_objects": [int, int],         # zero-based indices of the two closest objects to the agent's current position of (x, y).
    "closest_waypoints": [int, int],       # indices of the two nearest waypoints.
    "distance_from_center": float,         # distance in meters from the track center 
    "is_crashed": Boolean,                 # Boolean flag to indicate whether the agent has crashed.
    "is_left_of_center": Boolean,          # Flag to indicate if the agent is on the left side to the track center or not. 
    "is_offtrack": Boolean,                # Boolean flag to indicate whether the agent has gone off track.
    "is_reversed": Boolean,                # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
    "heading": float,                      # agent's yaw in degrees
    "objects_distance": [float, ],         # list of the objects' distances in meters between 0 and track_len.
    "objects_heading": [float, ],          # list of the objects' headings in degrees between -180 and 180.
    "objects_left_of_center": [Boolean, ], # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
    "objects_location": [(float, float),], # list of object locations [(x,y), ...].
    "objects_speed": [float, ],            # list of the objects' speeds in meters per second.
    "progress": float,                     # percentage of track completed
    "speed": float,                        # agent's speed in meters per second (m/s)
    "steering_angle": float,               # agent's steering angle in degrees
    "steps": int,                          # number steps completed
    "track_length": float,                 # track length in meters.
    "track_width": float,                  # width of the track
    "waypoints": [(float, float), ]        # list of (x,y) as milestones along the track center

}
"""

import math

def reward_function(params):
    SPEED_THRESHOLD = 6
    STEERING_THRESHOLD = 15
    DIRECTION_THRESHOLD = 15.0
# --------- Start Params ---------
    all_wheels_on_track = params['all_wheels_on_track'] # bool

    left_side = params['is_left_of_center'] # bool to determine if on left or right of track
    
    waypoints = params['waypoints']

    closest_waypoint = params['closest_waypoints']
    
    current_waypoint = waypoints[closest_waypoint[0]]

    next_waypoint = waypoints[closest_waypoint[1]]

    car_direction = ['heading']

    steering = abs(params['steering_angle'])

    speed = params['speed']

    track_progress = params ['progress']

    reward = 1  # initial reward
    punishment = 1 # used to penalize

# --------- End Params ---------

    # Give a big reward if you finished the track!

    
    
    #Make sure direction of car is that of track
    track_heading = math.atan2(next_waypoint[1] - current_waypoint[1], next_waypoint[0] - current_waypoint[0])
    track_heading = math.degrees(track_heading)
    #Compare correct direction V direction of car
    heading_delta = abs(track_heading - car_direction)

    if heading_delta > DIRECTION_THRESHOLD:
        punishment= 1 - (heading_delta / 50)

        if punishment < 0 or punishment > 1:
            punishment = 0
        
        reward = reward * punishment

    if track_progress == 100:  # reward getting to the end
        reward = reward + 150

    if speed < SPEED_THRESHOLD:  # Reward going fast
        reward = reward * 0.8

    if steering > STEERING_THRESHOLD:  # Reward not steering as much
        reward = reward * 0.7
    
    
    if left_side:  # reward being on left side of the track 
        reward = reward * 1.4
    else:
        reward = reward * 0.8

    if not (all_wheels_on_track):  # return almost 0 if car crashed
        reward = 0.0001
    
    # Sanity Check 
    if reward < 0:
        reward = 0

    return float(reward)

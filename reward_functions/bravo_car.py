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
    direction_stearing = params['steering_angle']
    speed = params['speed']
    steps = params['steps']
    progress = params['progress']
    left_of_center = params['is_left_of_center']

    all_wheels_on_track = params['all_wheels_on_track']

    waypoints = params['waypoints']    
    closest_waypoints = params['closest_waypoints']    
    heading = params['heading']

    ABS_STEERING_THRESHOLD = 15    
    SPEED_TRESHOLD = 5    
    TOTAL_NUM_STEPS = 85   
    DIRECTION_THRESHOLD = 10.0 

    reward = 1.0   
    penalty = 1    

    # Calculate the direction of the center line based on the closest waypoints    
    next_point = waypoints[closest_waypoints[1]]    
    prev_point = waypoints[closest_waypoints[0]]    
    
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians    
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])     # Convert to degree    
    track_direction = math.degrees(track_direction)    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)    # Penalize the reward if the difference is too large    
    
    if direction_diff > DIRECTION_THRESHOLD:        
        penalty = 1 - (direction_diff / 50)        
        if penalty < 0 or penalty > 1:            
            penalty = 0        
        reward *= penalty    

    if progress == 100:        
        reward += 100    

    if left_of_center:  # reward being on left side of the track 
        reward = reward * 1.4
    else:
        reward = reward * 0.8

    if speed < SPEED_TRESHOLD:
        reward = reward * 0.8
    
    if not all_wheels_on_track:
        reward = 0.00001

    if reward < 0:  # Sanity Check
        reward = 0


    return reward

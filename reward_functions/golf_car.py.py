import math

WAYPOINTS =[
       [2.88738855, 0.72646774],
       [3.16759122, 0.70478649],
       [3.45517317, 0.69217863],
       [3.75325158, 0.68581005],
       [4.07281434, 0.68360819],
       [4.50000223, 0.68376092],
       [4.54999507, 0.68377879],
       [5.11738115, 0.69080411],
       [5.44798256, 0.7112322 ],
       [5.71126558, 0.7422347 ],
       [5.94137211, 0.78496462],
       [6.1491271 , 0.84078035],
       [6.33675893, 0.91066736],
       [6.50351669, 0.99483994],
       [6.64762588, 1.09336367],
       [6.76714849, 1.20640158],
       [6.85790417, 1.33508669],
       [6.92193762, 1.47646609],
       [6.96026824, 1.62797346],
       [6.96689958, 1.7888072 ],
       [6.92976742, 1.95515434],
       [6.85379617, 2.11910271],
       [6.72693273, 2.26841633],
       [6.56582731, 2.3979065 ],
       [6.38075512, 2.50632652],
       [6.18037171, 2.5960265 ],
       [5.97126499, 2.67207187],
       [5.75829177, 2.74110301],
       [5.55841177, 2.81013238],
       [5.36004947, 2.88360578],
       [5.16333131, 2.96218803],
       [4.96844903, 3.04682634],
       [4.77552032, 3.13832543],
       [4.5846244 , 3.2374528 ],
       [4.39562481, 3.34419701],
       [4.20825035, 3.45789343],
       [4.02216522, 3.57740375],
       [3.83712807, 3.70184192],
       [3.68186141, 3.80970389],
       [3.52529227, 3.91179837],
       [3.36674073, 4.00606413],
       [3.20532486, 4.09041474],
       [3.0401252 , 4.16335643],
       [2.87024421, 4.22393077],
       [2.69486335, 4.27162279],
       [2.51319321, 4.30602365],
       [2.32452568, 4.32672382],
       [2.12696309, 4.33080298],
       [1.91810508, 4.31381212],
       [1.69471913, 4.26740868],
       [1.45416273, 4.17400849],
       [1.21119005, 4.00653223],
       [1.01922953, 3.74402202],
       [0.92220549, 3.42050544],
       [0.88926604, 3.10443889],
       [0.89600747, 2.82076036],
       [0.92404943, 2.56281185],
       [0.96605253, 2.32460305],
       [1.01802833, 2.11228544],
       [1.08079017, 1.91512981],
       [1.15513698, 1.73107571],
       [1.24162317, 1.56014807],
       [1.34112998, 1.40323884],
       [1.45472589, 1.2610932 ],
       [1.58653095, 1.13641183],
       [1.74472608, 1.03228688],
       [1.92655529, 0.94305481],
       [2.13282228, 0.86779425],
       [2.36411252, 0.80679887],
       [2.61751276, 0.75992145],
       [2.88738855, 0.72646774]]
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

def reward_function(params):
    
    
    on_track = params['all_wheels_on_track']
    x = params["x"]
    y = params['y']
    closest_waypoints = params['closest_waypoints']
    car_orientation = params['heading']

    
    reward = 1e-3
    
    rabbit = [0,0]
    pointing = [0,0]
        
    # Reward when yaw (car_orientation) is pointed to the next waypoint IN FRONT.
    
    # Find nearest waypoint coordinates
    closest_point = closest_waypoints[0]
    rabbit = [WAYPOINTS[closest_point], WAYPOINTS[closest_point]]
    
    radius = math.hypot(x - rabbit[0], y - rabbit[1])
    
    pointing[0] = x + (radius * math.cos(car_orientation))
    pointing[1] = y + (radius * math.sin(car_orientation))
    
    vector_delta = math.hypot(pointing[0] - rabbit[0], pointing[1] - rabbit[1])
    
    # Max distance for pointing away will be the radius * 2
    # Min distance means we are pointing directly at the next waypoint
    # We can setup a reward that is a ratio to this max.
    
    if vector_delta == 0:
        reward += 1
    else:
        reward += ( 1 - ( vector_delta / (radius * 2)))
    return float(reward)

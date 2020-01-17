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


TYPE_TRACK = {
    'straight': [0,1,2,3,4,5,6,7,8,9,10,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,54,55,56,57,58,59,60,68,69],
    'curve':[11,12,13,14,15,16,17,18,19,20,21,22,23,24,41,42,43,44,45,46,47,48,49,50,51,52,53,61,62,63,64,65,66,67]
}

def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    steps = params['steps']
    progress = params['progress']
    speed = params['speed']
    closest_points = params['closest_waypoints']
    first_point = WAYPOINTS[closest_points[0]]
    second_point = WAYPOINTS[closest_points[1]]
    heading = params['heading']
    DIRECTION_THRESHOLD = 10
    penalty = 1
    
    
    if all_wheels_on_track and steps > 0:
        reward = ((progress / steps) * 100) + speed ** 2
    else:
        reward = 0.000001

    def check_direction(second_point=second_point, first_point=first_point,
                        car_direction=heading, reward=reward, penalty=penalty):

        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians    
        track_direction = math.atan2(second_point[1] - first_point[1], second_point[0] - first_point[0])     # Convert to degree    
        track_direction = math.degrees(track_direction)    # Calculate the difference between the track direction and the heading direction of the car
        direction_diff = abs(track_direction - heading)    # Penalize the reward if the difference is too large    
        
        if direction_diff > DIRECTION_THRESHOLD:        
            penalty = 1 - (direction_diff / 50)        
            if penalty < 0 or penalty > 1:            
                penalty = 0.0001        
            reward *= penalty
        else:
            reward *= 1.2 # bump if you are going the right direction
    

        return float(reward)


    def check_speed(reward=reward, closest_points=closest_points, speed=speed):
        current_point = closest_points[0]
        curve = TYPE_TRACK['curve']
        straight = TYPE_TRACK['straight']

        is_curve = False
        is_straight = False

        if current_point in curve:
            is_curve = True
        
        if current_point in straight:
            is_straight = True

        
        if is_curve and speed > 6.7:
            reward *= 0.25
        
        if is_straight and speed < 6.7:
            reward *= 0.25
        
        return float(reward)



    reward = check_direction(second_point=second_point, first_point=first_point,
                        car_direction=heading, reward=reward, penalty=penalty)
    
    reward = check_speed(reward=reward, closest_points=closest_points, speed=speed)
    
    return float(reward)
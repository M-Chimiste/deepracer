import math


def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    steps = params['steps']
    progress = params['progress']
    speed = params['speed']
    waypoints = params['waypoints']
    closest_points = params['closest_waypoints']
    first_point = waypoints[closest_points[0]]
    second_point = waypoints[closest_points[1]]
    heading = params['heading']
    DIRECTION_THRESHOLD = 15
    penalty = 1
    
    
    if all_wheels_on_track and steps > 0:
        reward = ((progress / steps) * 100) + speed ** 3
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
                penalty = 0        
            reward *= penalty
        else:
            reward *= 1.2 # bump if you are going the right direction
        return float(reward)



    reward = check_direction(second_point=second_point, first_point=first_point,
                        car_direction=heading, reward=reward, penalty=penalty)
    
    return float(reward)
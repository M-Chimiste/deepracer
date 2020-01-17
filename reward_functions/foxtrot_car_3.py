def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    steps = params['steps']
    progress = params['progress']
    speed = params['speed']
    steering_angle = params['steering_angle']

    if all_wheels_on_track and steps > 0:
        reward =  ((progress / steps) * 100)
    else:
        reward =  0.000001
    

    if abs(steering_angle) > 15:
        reward = 0.8 * reward
    
    if speed < 3.0:
        reward = 0.7 * reward

    return float(reward)

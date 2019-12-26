def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    steps = params['steps']
    progress = params['progress']
    speed = params['speed']

    if all_wheels_on_track and steps > 0:
        reward = ((progress / steps) * 100) ** speed
    else:
        reward = 0.000001
    
    return float(reward)
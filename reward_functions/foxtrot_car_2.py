def reward_function(params):
    all_wheels_on_track = params['all_wheels_on_track']
    steps = params['steps']
    progress = params['progress']
    speed = params['speed']
    left_of_center = params['is_left_of_center']

    if all_wheels_on_track and steps > 0:
        reward =  ((progress / steps) * 100) + speed ** 2
    else:
        reward =  0.000001
    

    if not left_of_center:
        reward = 0.8 * reward

    return float(reward)

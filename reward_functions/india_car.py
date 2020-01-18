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


def dist(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


# thanks to https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates
def rect(r, theta):
    """
    theta in degrees
    returns tuple; (float, float); (x,y)
    """

    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


# thanks to https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates
def polar(x, y):
    """
    returns r, theta(degrees)
    """

    r = (x ** 2 + y ** 2) ** .5
    theta = math.degrees(math.atan2(y,x))
    return r, theta


def angle_mod_360(angle):
    """
    Maps an angle to the interval -180, +180.
    Examples:
    angle_mod_360(362) == 2
    angle_mod_360(270) == -90
    :param angle: angle in degree
    :return: angle in degree. Between -180 and +180
    """

    n = math.floor(angle/360.0)

    angle_between_0_and_360 = angle - n*360.0

    if angle_between_0_and_360 <= 180.0:
        return angle_between_0_and_360
    else:
        return angle_between_0_and_360 - 360


def get_waypoints_ordered_in_driving_direction(params, waypoints=WAYPOINTS):
    # waypoints are always provided in counter clock wise order
    if params['is_reversed']: # driving clock wise.
        return list(reversed(waypoints))
    else: # driving counter clock wise.
        return waypoints


def up_sample(waypoints, factor):
    """
    Adds extra waypoints in between provided waypoints
    :param waypoints:
    :param factor: integer. E.g. 3 means that the resulting list has 3 times as many points.
    :return:
    """
    p = waypoints
    n = len(p)

    return [[i / factor * p[(j+1) % n][0] + (1 - i / factor) * p[j][0],
             i / factor * p[(j+1) % n][1] + (1 - i / factor) * p[j][1]] for j in range(n) for i in range(factor)]


def get_target_point(params):
    waypoints = up_sample(get_waypoints_ordered_in_driving_direction(params, WAYPOINTS), 20)

    car = [params['x'], params['y']]

    distances = [dist(p, car) for p in waypoints]
    min_dist = min(distances)
    i_closest = distances.index(min_dist)

    n = len(waypoints)

    waypoints_starting_with_closest = [waypoints[(i+i_closest) % n] for i in range(n)]

    r = params['track_width'] * 0.9

    is_inside = [dist(p, car) < r for p in waypoints_starting_with_closest]
    i_first_outside = is_inside.index(False)

    if i_first_outside < 0:  # this can only happen if we choose r as big as the entire track
        return waypoints[i_closest]

    return waypoints_starting_with_closest[i_first_outside]


def get_target_steering_degree(params):
    tx, ty = get_target_point(params)
    car_x = params['x']
    car_y = params['y']
    dx = tx-car_x
    dy = ty-car_y
    heading = params['heading']

    _, target_angle = polar(dx, dy)

    steering_angle = target_angle - heading

    return angle_mod_360(steering_angle)


def score_steer_to_point_ahead(params):
    best_stearing_angle = get_target_steering_degree(params)
    steering_angle = params['steering_angle']

    error = (steering_angle - best_stearing_angle) / 60.0  # 60 degree is already really bad

    score = 1.0 - abs(error)

    return max(score, 0.01)  # optimizer is rumored to struggle with negative numbers and numbers too close to zero


def reward_function(params):
    on_track = params['all_wheels_on_track']
    reward = score_steer_to_point_ahead(params)
    if on_track:
        return float(reward)
    else:
        reward = 0.0001
        return float(reward)

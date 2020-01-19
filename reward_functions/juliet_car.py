import math

WAYPOINTS =[[2.88517874, 0.70969365],
       [3.16352253, 0.6941537 ],
       [3.43313686, 0.68823119],
       [3.73804833, 0.68548309],
       [4.10748697, 0.68438309],
       [4.4112053 , 0.68402702],
       [4.70859097, 0.68388315],
       [5.25879176, 0.68554663],
       [5.50082691, 0.69724613],
       [5.73246514, 0.72064555],
       [5.96323271, 0.76195407],
       [6.17363769, 0.82146936],
       [6.35766926, 0.89693362],
       [6.51645028, 0.98654135],
       [6.65191256, 1.08923805],
       [6.76510607, 1.20448784],
       [6.85585493, 1.33206465],
       [6.92243248, 1.47191332],
       [6.96129471, 1.62371412],
       [6.96643383, 1.78598246],
       [6.92892823, 1.95361385],
       [6.85351802, 2.11861016],
       [6.73590113, 2.27236311],
       [6.58230548, 2.40817611],
       [6.40052226, 2.5226911 ],
       [6.19903524, 2.61649445],
       [5.98562853, 2.69409169],
       [5.76663451, 2.76272803],
       [5.56620966, 2.82850207],
       [5.36678143, 2.89814869],
       [5.16868621, 2.9729828 ],
       [4.97229967, 3.05435165],
       [4.77810131, 3.14365668],
       [4.5869895 , 3.24278341],
       [4.3991633 , 3.3505198 ],
       [4.21473213, 3.46560154],
       [4.03365156, 3.5867667 ],
       [3.85572697, 3.71282115],
       [3.68060425, 3.84263414],
       [3.53054803, 3.94977492],
       [3.37958965, 4.05066132],
       [3.2271022 , 4.14314338],
       [3.07225431, 4.22573016],
       [2.91381127, 4.29712498],
       [2.75006109, 4.35635002],
       [2.57839948, 4.40202027],
       [2.39483514, 4.43181978],
       [2.1931077 , 4.44111982],
       [1.96426358, 4.41994182],
       [1.70647996, 4.35075189],
       [1.44376776, 4.21845884],
       [1.20672793, 4.01832988],
       [1.02190428, 3.75227656],
       [0.91810319, 3.43634523],
       [0.88025101, 3.11930699],
       [0.88710714, 2.83214191],
       [0.91721072, 2.57310395],
       [0.96293881, 2.31103478],
       [1.01220395, 2.10571041],
       [1.07373688, 1.90995457],
       [1.14856781, 1.72569856],
       [1.23682933, 1.55537176],
       [1.33850966, 1.40041153],
       [1.45417005, 1.26143494],
       [1.58564605, 1.13865247],
       [1.73769319, 1.03244965],
       [1.91119243, 0.93938539],
       [2.11015474, 0.85907232],
       [2.3394868 , 0.79246068],
       [2.60144227, 0.74185631],
       [2.88517874, 0.70969365]]
UP_SAMPLE_FACTOR = 1

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
    waypoints = up_sample(get_waypoints_ordered_in_driving_direction(params, WAYPOINTS), UP_SAMPLE_FACTOR)

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
    
    if on_track:
        direction = score_steer_to_point_ahead(params)
        reward = ((progress / steps) * 100) + direction ** 2
        return float(reward)
    else:
        reward = 0.0001
        return float(reward)

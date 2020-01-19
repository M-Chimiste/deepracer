import math



WAYPOINTS = [[2.88517874, 0.70969365],
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


def reward_function(params):


    # Read input parameters
    steering = params['steering_angle']
    yaw = params['heading']
    all_wheels_on_track = params['all_wheels_on_track']
    waypoints = WAYPOINTS
    closest_waypoints = params['closest_waypoints']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    progress = params['progress']
    x = params['x']
    y = params['y']
    
    # Let's start rewarding our solution!
    reward = 0

    # Give a high reward if no wheels go off the track. IF it's not on track, dont even continue.
    if all_wheels_on_track:
        reward += 5
    else:
        reward = -1   
        return float(reward)
        
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward += 10
    elif distance_from_center <= marker_2:
        reward += 5
    elif distance_from_center <= marker_3:
        reward += 1
    else:
        reward = -1  # likely crashed/ close to off track

    #Closest points X and Y Coordinates. We will get an average of the next 5 points in front of us. 
    next_point = closest_waypoints[1]
    len_maxpoints = len(waypoints)
    iteractions = 3 #arbitrary number. 

    sum_X = 0
    sum_Y = 0
    for i in range(next_point, next_point+iteractions,1):
        w = waypoints[i % len_maxpoints] #use mod to avoid errors. Think about completing one full lap. 
        sum_X += w[0] #Getting X coordinate. 
        sum_Y += w[1] #Getting Y coordinate. 

    C_X = sum_X / iteractions 
    C_Y = sum_Y / iteractions


    #Calculate the distance from the car to the next point
    distance = math.hypot(x - C_X, y - C_Y)

    #Calculate the predicted vehicle location considering the current yaw. Yaw and Steering are in angles, convert to radians first.
    P_X = x + (distance * math.cos(math.radians(yaw + steering)))
    P_Y = y + (distance * math.sin(math.radians(yaw + steering)))

    predicted_distance = math.hypot(C_X - P_X, C_Y - P_Y)

    if predicted_distance <= marker_1: #vehicle is pointing to the right direction. 
        reward += 10
    elif predicted_distance <= marker_2:
    	reward += 5
    elif predicted_distance <= marker_3:
    	reward += 1
    else:                      #vehicle is pointing to the wrong direction. 
        reward = -1 * (predicted_distance / (distance * 2))
    

    return float(reward)

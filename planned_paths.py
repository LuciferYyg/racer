def reward_function(params):

    center_variance = params["distance_from_center"] / params["track_width"]

    left_lane = [26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,66,67,68,69,70,71,72,73,78,79,80,81,82,83,84,85,86,104,105,106,107,108,109]
    right_lane = [51,52,53,54,55,56,57]
    center_lane = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,48,49,50,58,59,60,61,62,63,64,65,74,75,76,77,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127]

    low_speed=[21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,75,76,77,78,79,80,81,82,83,84,85]
    mid_speed=[16,17,18,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110]
    fast_speed=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67]
    
    reward = 0
    #车在轨道里
    if params["all_wheels_on_track"]:
        #车靠近左侧规划点，且车在左侧
        if params["closest_waypoints"][1] in left_lane and params["is_left_of_center"]:
            reward = 70
        #车靠近右侧规划点，且车在左侧
        elif params["closest_waypoints"][1] in right_lane and not params["is_left_of_center"]:
            reward = 70
        #车靠近中间规划点，且车在中间
        elif params["closest_waypoints"][1] in center_lane and center_variance < 0.3:
            reward = 70
        #车的位置与规划点不符，则低分
        else:
            reward = 0.001
        #现在设置是低速1.5-2.0，中速2.25-2.75，高速3.5-4.0
        #下一个点是低速点，且当前速度符合低速挡要求，+=10
		if params["closest_waypoints"][1] in low_speed and params["speed"]>=1.0 and params["speed"]<=1.5:
			reward = reward + 30
        #下一个点是中速点，且当前速度符合中速挡要求
        elif params["closest_waypoints"][1] in mid_speed and params["speed"]>=1.75 and params["speed"]<=2.25:
        	reward = reward + 30
        #下一个点是高速点，且当前速度符合高速挡要求
        elif params["closest_waypoints"][1] in fast_speed and params["speed"]>=2.5 and params["speed"]<=3.0:
        	reward = reward + 30
        #else车速与点配速不符，0.01
        else :
        	reward = reward + 0.001
        
    else:
        reward = 0.01
        
    
    
    
    #如果规划速度就不要这个速度自学习
    #reward *= params["speed"]**2
    

    return float(reward)
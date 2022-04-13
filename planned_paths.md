
将赛道分成左、中、右三个部分。以赛道中轴线为中心，超过中轴线一定比例就算做左赛道或右赛道。

将速度也分为两个部分，一个是快速，一个是慢速。

赛道有118个坐标，将一部分坐标归在左赛道，一部分在中赛道，另一部分在右赛道。然后也可以将同时将坐标分为哪些属于快速，哪些属于慢速。

1. 根据distance_from_center和track_width的比例判断中心赛道区域；
2. 根据is_left_of_center和not is_left_of_center判断左赛道区域和右赛道区域；
3. 根据closest_waypoints的[1]的值判断下一个checkpoint的值；
4. 建立数组：left[], center[], right[], fast[], slow[]，将118个坐标点根据你设计的路线情况，填入数组内；
5. 设置奖励值，比如赛车当前如果处理left[]数组内，并且is_left_of_center == true，那么就给予奖励。

  一个人补全一个位置数组，补全两个速度数组，以及对应写两个速度的对应奖惩 

  速度数组的名字也可以事先统一一下，比如叫s15，就表示速度（speed）为1.5左右（1.5-1.8）的数组，
  s20表示速度为2.0左右（1.8-2.3）的数组，每个速度数组都预设一个速度上下限，超过上限或不足下限就扣分，在这范围内就加分

    然后速度数组也可以不用完全闭合，比如说看那个配速图，0-14直线（配速4.0），之后准备转弯，会在点15到点22减速，
    弯道点22到点38（配速1.5），那么点15-22就可以不用纳入配速数组，让他自己学习，因为已知0-14是配速4.0，已知点22-38配速1.5，
    如果在22-38不满足配速要求，那么他肯定要自己学习到一个减速的过程
    所以如果这么想的话，觉得速度数组又不用那么多了，3个（高中低速）就足够了
    低速1.5到2.0（主要是转弯），中速2.25到2.75（主要是左边的赛道），高速3.5到4（主要是直线）
    如果每个配速粒度都开一个数组，有些速度数组的点应该很少,这些大家都可以讨论






​    
```python
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
```


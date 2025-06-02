def reward_function(params):
    all_wheels_on = params['all_wheels_on']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle'])  # Absolute angle
    speed = params['speed']
    progress = params['progress']
    steps = params['steps']
    
    reward = 1e-3

    if not all_wheels_on:
        return reward

    # Centering
    if distance_from_center <= 0.1 * track_width:
        reward = 1.5
    elif distance_from_center <= 0.25 * track_width:
        reward = 1.0
    else:
        reward = 0.5

    # Penalize hard turns
    if steering > 20:
        reward *= 0.8

    # Reward faster speed (now that it can go higher)
    if speed >= 3.5:
        reward *= 1.8
    elif speed >= 2.5:
        reward *= 1.5
    elif speed >= 1.5:
        reward *= 1.2

    # Efficiency bonus
    if steps > 0:
        reward += (progress / steps) * 10.0

    return float(reward)
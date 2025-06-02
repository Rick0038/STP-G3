def reward_function(params):
    """
    Reward function for AWS DeepRacer:
    - Rewards staying on track
    - Encourages driving closer to the center
    - Penalizes sharp zigzag steering
    - Rewards faster progress
    - Encourages faster speed
    """
    # Extract params
    all_wheels_on = params['all_wheels_on']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle'])  # Only magnitude
    speed = params['speed']
    progress = params['progress']
    steps = params['steps']
    
    # Default reward
    reward = 1e-3

    # Check if the car is on the track
    if not all_wheels_on:
        return reward  # immediately return minimal reward

    # 1. Reward staying near the center
    center_threshold_1 = 0.1 * track_width
    center_threshold_2 = 0.25 * track_width
    if distance_from_center <= center_threshold_1:
        reward = 1.5
    elif distance_from_center <= center_threshold_2:
        reward = 1.0
    else:
        reward = 0.5  # Near the edge

    # 2. Penalize excessive steering (zigzag)
    if steering > 20:
        reward *= 0.8

    # 3. Encourage speed
    if speed >= 3.0:
        reward *= 1.5
    elif speed >= 2.0:
        reward *= 1.2

    # 4. Reward efficient progress
    if steps > 0:
        progress_reward = (progress / steps) * 10.0
        reward += progress_reward

    return float(reward)
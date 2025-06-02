from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from car_env import CarEnv

env = CarEnv()
check_env(env)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=50000)
model.save("car_agent")
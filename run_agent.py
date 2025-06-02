import time
from stable_baselines3 import PPO
from car_env import CarEnv

env = CarEnv()
model = PPO.load("car_agent")

obs = env.reset()
for _ in range(1000):
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()
    time.sleep(0.05)
    if done:
        obs = env.reset()
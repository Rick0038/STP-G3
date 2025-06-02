import gym
import numpy as np
from gym import spaces
import pygame
import math

WIDTH, HEIGHT = 400, 400
TARGET_POS = np.array([350, 350])

class CarEnv(gym.Env):
    def __init__(self):
        super(CarEnv, self).__init__()
        self.screen = None
        self.car_pos = np.array([50.0, 50.0])
        self.car_angle = 0.0
        self.speed = 0.0

        # Actions: [steering, throttle]
        self.action_space = spaces.Box(low=np.array([-1.0, -1.0]),
                                       high=np.array([1.0, 1.0]),
                                       dtype=np.float32)
        # Observations: [x, y, angle, speed, dx, dy]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32)

    def reset(self):
        self.car_pos = np.array([50.0, 50.0])
        self.car_angle = 0.0
        self.speed = 0.0
        return self._get_obs()

    def _get_obs(self):
        dx, dy = TARGET_POS - self.car_pos
        return np.array([
            self.car_pos[0],
            self.car_pos[1],
            self.car_angle,
            self.speed,
            dx,
            dy
        ], dtype=np.float32)

    def step(self, action):
        steer, throttle = np.clip(action, -1, 1)
        self.speed += throttle * 0.5
        self.speed = np.clip(self.speed, 0, 5)
        self.car_angle += steer * 5  # steering turns car
        rad = math.radians(self.car_angle)
        self.car_pos[0] += self.speed * math.cos(rad)
        self.car_pos[1] += self.speed * math.sin(rad)

        # Compute reward
        distance = np.linalg.norm(TARGET_POS - self.car_pos)
        done = distance < 15 or not (0 <= self.car_pos[0] <= WIDTH and 0 <= self.car_pos[1] <= HEIGHT)
        reward = -distance * 0.01
        if distance < 15:
            reward += 10  # bonus for reaching the goal
        return self._get_obs(), reward, done, {}

    def render(self, mode='human'):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill((255, 255, 255))
        pygame.draw.circle(self.screen, (0, 255, 0), TARGET_POS.astype(int), 10)
        car_x, car_y = self.car_pos.astype(int)
        pygame.draw.circle(self.screen, (0, 0, 255), (car_x, car_y), 5)
        pygame.display.flip()

    def close(self):
        if self.screen:
            pygame.quit()
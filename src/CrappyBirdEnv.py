import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete

import numpy as np
import random
import os

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy


class CrappyBirdEnv(Env):

    def __init__(self, root, game_window):
        self.action_space = Discrete(2)
        # 0 = Y position of the bird | 1 = Distance from the bird to the next pipe | 2 = Y position of the hole
        self.observation_space = MultiDiscrete([641, 481, 641])
        self.state = [0, 0, 0]
        self.root = root
        self.game_window = game_window

    def step(self, action):
        #print("Jump" if action == 1 else "No jump")
        self.state = self.game_window.tick(action)
        print('State {} - Lose {}'.format(self.state, self.game_window.stop))

        return self.state, 1, self.game_window.stop, {}

    def render(self, **kwargs):
        self.root.update_idletasks()
        self.root.update()

    def reset(self):
        self.action_space = Discrete(2)
        # 0 = Y position of the bird | 1 = Distance from the bird to the next pipe | 2 = Y position of the hole
        self.observation_space = MultiDiscrete([641, 481, 641])
        self.state = 0
        self.game_window.reset()
        return self.state

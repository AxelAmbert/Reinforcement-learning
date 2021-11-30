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
        self.observation_space = Box(-np.inf, np.inf, shape=(3,))

        # print(self.observation_space.sample())
        self.root = root
        self.game_window = game_window

    def _get_observation(self, action):
        h_dist, v_dist_one, v_dist_two = self.game_window.tick(action)
        return np.array([h_dist, v_dist_one, v_dist_two])
        h_dist /= self.game_window.screen_size[0]
        v_dist_one /= self.game_window.screen_size[1]
        v_dist_two /= self.game_window.screen_size[1]

    def step(self, action):
        # print("Jump" if action == 1 else "No jump")
        obs = self._get_observation(action)
        #print('State {} - Lose {}'.format(obs, self.game_window.stop))

        return obs, 1, self.game_window.stop, {}

    def render(self, **kwargs):
        self.root.update_idletasks()
        self.root.update()

    def reset(self):
        # 0 = Y position of the bird | 1 = Distance from the bird to the next pipe | 2 = Y position of the hole
        # self.observation_space = MultiDiscrete([641, 481, 641])
        self.game_window.reset()
        return self._get_observation(0)

    def close(self):
        print('close ?')
        exit(0)

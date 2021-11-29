import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete

import numpy as np
import random
import os

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

from src.GameInfo import GameInfo
from src.Utils import Utils


class CrappyBirdEnv(Env):

    def __init__(self, root, game_window):
        self.action_space = Discrete(2)
        # 0 = Y position of the bird | 1 = Distance from the bird to the next pipe | 2 = Y position of the hole
        self.observation_space = MultiDiscrete([481, 641, 641]) #[641, 481, 641, 641]
        self.root = root
        self.game_window = game_window
        self.state = game_window.tick(0)
        self.last_score = 0
        self.total_reward = 0
        self.last_reward = 0

    # This function attenuate reward if the bird is close to the pipe
    def attenuate_reward(self, reward, distance_x):
        reversed_normalized_value = 1 - (((GameInfo.window_size.x - 100) - distance_x) / (GameInfo.window_size.x - 100))

        if reward > self.last_reward:
            diff = reward - self.last_reward
            diff *= reversed_normalized_value
            return diff + self.last_reward
        else:
            return reward * reversed_normalized_value

    def compute_reward(self):
        next_pipe_pos = self.game_window.pipes[-1].positions[1].y + self.game_window.pipes[-1].size.y / 2
        player_pos = self.game_window.player.get_player_pos()
        wanted_pos = next_pipe_pos + (GameInfo.window_size.y / 8) - self.game_window.player.size.y / 2
        distance_y = abs(int(wanted_pos - player_pos))
        distance_x = self.game_window.get_distance_from_pipe()

        value = (GameInfo.window_size.y - distance_y) / GameInfo.window_size.y

        if value > 0.9:
            return Utils.clamp(value, 0, 1)
        #print('Coefficient {} - {}'.format(value, self.attenuate_reward(value, distance_x)))

        #value = self.attenuate_reward(value, distance_x)

        coeff = 1 - (((GameInfo.window_size.x - 100) - distance_x) / (GameInfo.window_size.x - 100))
        value *= coeff
        self.last_reward = value
        return value
        #print('Value ? {} - Distance ? {}'.format(value, distance))

        #return value

    def step(self, action):
        #print("Action choisie {}".format("Jump" if action == 1 else "Nothing"))

        #print("Jump" if action == 1 else "No jump")
        self.state = self.game_window.tick(action)
        #print('State {} - Lose {} - Pos ? {}'.format(self.state, self.game_window.stop, int(self.game_window.player.pos.y - self.game_window.player.size.y / 2)))
        reward = self.compute_reward()
        if self.last_score != self.game_window.score.score:
            self.last_score = self.game_window.score.score
            #reward += 10
        print('Reward {} - total {} - state {}'.format(reward, self.total_reward, self.state))
        self.total_reward += reward
        return self.state, reward, self.game_window.stop, {'reward': reward, 'total_reward': self.total_reward}
        #return [self.game_window.player.get_clamped_pos()], 1 + bonus, self.game_window.stop, {}

    def render(self, **kwargs):
        self.root.update_idletasks()
        self.root.update()

    def reset(self):
        self.action_space = Discrete(2)
        # 0 = Y position of the bird | 1 = Distance from the bird to the next pipe | 2 = Y position of the hole
        self.observation_space = MultiDiscrete([481, 641, 641])
        self.state = 0
        self.game_window.reset()
        self.state = self.game_window.tick(0)
        self.last_score = 0
        print('reset')
        return self.state

import glob
import math
import os
import sys
import time

from tkinter import *

import pyglet
from gym.wrappers import Monitor
from pyglet.gl import GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, glBlendFunc, glEnable, glClear, \
    GL_COLOR_BUFFER_BIT
from pyglet.window import key
import gym
import os
from stable_baselines3.common.policies import ActorCriticPolicy, register_policy
from pyglet import window, gl
from stable_baselines3 import PPO, DQN, TD3
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecVideoRecorder
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold, CheckpointCallback

from src.CrappyBirdEnv import CrappyBirdEnv
from src.GameInfo import GameInfo
from src.GameWindow import GameWindow
import datetime

from src.Pipe import Pipe
from src.Point import Point

default_screen_size = Point(1920, 1080)
default_window_size = Point(480, 640)

class CrappyBirdAI:

    def __init__(self):
        self.root = None
        self.AI_ON = True
        self.AI_FALSE = False
        self.jump = False
        self.display_mode = sys.argv[1] == 'game' or sys.argv[1] == 'play'
        self.chosen_algorithm = PPO
        if self.display_mode:
            self.init_window()
        self.game_window = self.init()
        self.delta = 0

    # def on_draw(self):
    #   self.root.clear()
    #    self.delta += pyglet.clock.tick()
    #    self.delta = 0
    #    self.game_window.draw()

    def update(self):
        self.game_window.tick(self.jump)
        self.jump = False

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            self.jump = True

    def get_latest_file(self, path):
        folder_path = path
        file_type = '\*zip'
        files = glob.glob(folder_path + file_type)

        return max(files, key=os.path.getctime)

    def init_window(self):
        self.root = pyglet.window.Window()
        self.root.set_size(default_window_size.x, default_window_size.y)
        glEnable(GL_BLEND)  # transparency
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency

    def load_last_model(self):
        PPO_Path = os.path.join('Training', 'Saved Models')
        env = CrappyBirdEnv()
        file = self.get_latest_file(PPO_Path)

        model = self.chosen_algorithm.load(file, env=env)
        return model, env

    def load_custom_model(self):
        log_path = os.path.join('Training', 'Logs')

        #env = SubprocVecEnv([lambda: CrappyBirdEnv() for _ in
        #                    range(computer_cores)])
        env = CrappyBirdEnv()
        # env = CrappyBirdEnv(self.root, self.game_window)

        # env = DummyVecEnv([lambda: env])


        model = self.chosen_algorithm('MlpPolicy', env, verbose=1, tensorboard_log=log_path)

        return model, env

    def render_test(self, model, env):

        env = CrappyBirdEnv()
        for episode in range(1000):
            obs = env.reset()
            done = False
            score = 0

            while not done:
                # env.render()
                time.sleep(1 / 200)
                action, _ = model.predict(obs, deterministic=True)
                obs, reward, done, info = env.step(action)
                self.root.dispatch_events()
                self.root.clear()
                env.render()
                self.root.flip()
                score += reward


    def play(self, ):
        model, env = self.load_last_model()

        self.render_test(model, env)

    def init(self, ):
        if self.root is None:
            GameInfo.init_info(default_window_size, self.AI_ON)
        else:
            height, width = self.root.get_size()

            GameInfo.init_info(Point(width, height), self.AI_ON)

        game_window = GameWindow()

        return game_window
        # return root, game_window

    def game(self, ):
        delta_tick = 0
        delta_draw = 0
        self.root.on_key_press = lambda symbol, modifiers: self.on_key_press(symbol, modifiers)

        while not AI.game_window.stop:
            delta = pyglet.clock.tick()
            delta_tick += delta
            delta_draw += delta
            self.root.dispatch_events()
            if delta_tick > 1 / 60:
                self.update()
                delta_tick = 0
            if delta_draw > 1 / 144:
                self.root.clear()
                self.game_window.draw()
                self.root.flip()
                delta_draw = 0
        #        pyglet.app.run()

        '''root.bind('<Key>', lambda e: enable_jump())
        self.update(game_window)
        while True:
           root.update_idletasks()
           root.update()'''

    def learn(self, ):
        model, env = self.load_custom_model()


        model.learn(total_timesteps=int(100000),)
        self.init_window()
        PPO_Path = os.path.join('Training', 'Saved Models',
                                'PPO_flappy_{}'.format(int(math.floor(datetime.datetime.now().timestamp()))))
        model.save(PPO_Path)
        self.render_test(model, env)
        # root.mainloop()


if __name__ == "__main__":
    AI = CrappyBirdAI()
    AI.__getattribute__(sys.argv[1])()

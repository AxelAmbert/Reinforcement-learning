import glob
import math
import os
import sys
import time
from tkinter import *

import gym
import os

from stable_baselines3 import PPO, DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

from src.CrappyBirdEnv import CrappyBirdEnv
from src.GameInfo import GameInfo
from src.GameWindow import GameWindow
import datetime

AI_ON = True
AI_FALSE = False
globals()['jump'] = False
GAME_MODE = False
chosen_algorithm = PPO


def update(root, window):
    window.tick(globals()['jump'])
    globals()['jump'] = False
    root.after(int(1000 / 60), lambda: update(root, window))


def enable_jump():
    globals()['jump'] = True

def get_latest_file(path):
    folder_path = path
    file_type = '\*zip'
    files = glob.glob(folder_path + file_type)

    return max(files, key=os.path.getctime)

def load_last_model(root, game_window):
    PPO_Path = os.path.join('Training', 'Saved Models')
    env = CrappyBirdEnv(root, game_window)
    file = get_latest_file(PPO_Path)

    model = chosen_algorithm.load(file, env=env)
    return model, env

def load_custom_model(root, game_window):
    env = CrappyBirdEnv(root, game_window)
    log_path = os.path.join('Training', 'Logs')

    # env = DummyVecEnv([lambda: env])
    model = chosen_algorithm('MlpPolicy', env, verbose=1, tensorboard_log=log_path)

    return model, env


def render_test(model, env):
    for episode in range(1000):
        obs = env.reset()
        done = False
        score = 0

        while not done:
            env.render()
            #time.sleep(1 / 60)
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            score += reward
            print(obs)
            print(action)
            print(score)
            print('')


def play_model():
    root, game_window = init()
    model, env = load_last_model(root, game_window)

    render_test(model, env)


def init():
    root = Tk()

    root.title("Crappy Bird")
    GameInfo.init_info(root, AI_ON)

    game_window = GameWindow(root)

    return root, game_window


def game():
    root, game_window = init()
    root.bind('<Key>', lambda e: enable_jump())

    update(root, game_window)
    while True:
        root.update_idletasks()
        root.update()


def learn():
    root, game_window = init()

    model, env = load_custom_model(root, game_window)

    model.learn(total_timesteps=1000000)

    PPO_Path = os.path.join('Training', 'Saved Models',  'PPO_flappy_{}'.format(math.floor(datetime.datetime.now().timestamp())))
    model.save(PPO_Path)
    render_test(model, env)
    # root.mainloop()


if sys.argv[1] == 'learn':
    learn()
elif sys.argv[1] == 'play':
    play_model()
elif sys.argv[1] == 'game':
    game()

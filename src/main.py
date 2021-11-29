import os
import sys
from tkinter import *

import gym
import os

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

from src.CrappyBirdEnv import CrappyBirdEnv
from src.GameInfo import GameInfo
from src.GameWindow import GameWindow

AI_ON = True
AI_FALSE = False
globals()['jump'] = False

GAME_MODE = False

def update(root, window):
    # print(window.tick(globals()['jump']))
    globals()['jump'] = False
    root.after(int(1 / 60), lambda: update(root, window))

def enable_jump():
    globals()['jump'] = True


def load_custom_model(root, game_window):
    env = CrappyBirdEnv(root, game_window)
    log_path = os.path.join('Training', 'Logs')

    # env = DummyVecEnv([lambda: env])
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=log_path)

    return model, env


def render_test(model, env):
    for episode in range(1000):
        obs = env.reset()
        done = False
        score = 0

        while not done:
            env.render()
            action, _ = model.predict(obs)
            obs, reward, done, info = env.step(action)
            score += reward
            print(obs)
            print(action)
            print(score)
            print('')


def play_model():
    root, game_window = init()
    model, env = load_custom_model(root, game_window)

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

    root.after(int(1 / 60), lambda: update(root, game_window))
    while True:
        root.update_idletasks()
        root.update()


def learn():
    root, game_window = init()

    model, env = load_custom_model(root, game_window)

    model.learn(total_timesteps=1000000)

    PPO_Path = os.path.join('Training', 'Saved Models', 'PPO_flappy')
    model.save(PPO_Path)
    # model = PPO.load(PPO_Path, env=env)

    render_test(model, env)
    # root.mainloop()


if sys.argv[1] == 'learn':
    learn()
elif sys.argv[1] == 'play':
    play_model()
elif sys.argv[1] == 'game':
    game()

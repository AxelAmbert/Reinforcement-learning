import os
import sys
from tkinter import *

import gym
import os

import keyboard
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
    print(window.tick(globals()['jump']))
    globals()['jump'] = False
    root.after(int(1000 / 60), lambda: update(root, window))

def enable_jump():
    globals()['jump'] = True


def load_custom_model(root, game_window):
    env = CrappyBirdEnv(root, game_window)
    log_path = os.path.join('Training', 'Logs')

    env = DummyVecEnv([lambda: env])
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=log_path)

    return model, env


def render_test(model, env):
    episodes = 100
    for episode in range(1, episodes + 1):
        obs = env.reset()
        done = False
        score = 0

        i = 0
        while not done:
            i += 1
            env.render()
            action, _ = model.predict(obs)
            obs, reward, done, info = env.step(action)
            score += reward
            print('Score {} - Reward {} - Done {} - State {}'.format(score, reward, done, obs))




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

    root.after(int(1000 / 60), lambda: update(root, game_window))
    while True:
        root.update_idletasks()
        root.update()



def learn():
    root, game_window = init()

    env, model = load_custom_model(root, game_window)

    model.learn(total_timesteps=1000000)

    PPO_Path = os.path.join('Training', 'Saved Models', 'PPO_Model_Cartpole')
    model.save(PPO_Path)
    del model
    model = PPO.load(PPO_Path, env=env)

    print('please press space')
    while True:
        key = keyboard.read_key()
        if key == 'space':  # You can put any key you like instead of 'space'
            break

    render_test(model, env)
    # root.mainloop()

if sys.argv[1] == 'learn':
    learn()
elif sys.argv[1] == 'play':
    play_model()
elif sys.argv[1] == 'game':
    game()

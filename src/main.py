import os
import sys
from time import sleep
from tkinter import *

import gym
import os

import keyboard
from stable_baselines3 import A2C, DQN, PPO
from stable_baselines3 import HerReplayBuffer
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold

from src.CrappyBirdEnv import CrappyBirdEnv
from src.GameInfo import GameInfo
from src.GameWindow import GameWindow


AI_ON = True
AI_FALSE = False
globals()['jump'] = False

GAME_MODE = False


chosen_algorithm = PPO
verbose = 1

def load_best_model(root, game_window):
    env = CrappyBirdEnv(root, game_window)
    log_path = os.path.join('Training', 'Logs')

    env = DummyVecEnv([lambda: env])
    PPO_Path = os.path.join('Training', 'Saved Models', 'Best')
    model = chosen_algorithm.load(PPO_Path, env=env)
    return model, env

def load_custom_model(root, game_window):
    log_path = os.path.join('Training', 'Logs')
    env = CrappyBirdEnv(root, game_window)
    env = DummyVecEnv([lambda: env])
    #env = DummyVecEnv([lambda: env, lambda: env, lambda: env])
    model = chosen_algorithm('MlpPolicy', env, verbose=1, tensorboard_log=log_path)
    return model, env


def pause():
    while True:
        key = keyboard.read_key()
        if key == 'space':  # You can put any key you like instead of 'space'
            break

def render_test(model, env, wait=True):
    episodes = 100

    if wait:
        pause()
    for episode in range(1, episodes + 1):
        obs = env.reset()
        done = False
        score = 0

        while not done:
            env.render()
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            score += reward
            #print('Score {} - Reward {} - Done {} - State {}'.format(score, reward, done, obs))
            #sleep(1/60)

        pause()




def play_model():
    root, game_window = init()
    model, env = load_best_model(root, game_window)

    render_test(model, env, False)



def init():
    root = Tk()

    root.attributes('-topmost', True)
    root.title("Crappy Bird")
    GameInfo.init_info(root, AI_ON)

    game_window = GameWindow(root)

    return root, game_window


def update(root, window):
    window.tick(globals()['jump'])
    globals()['jump'] = False
    root.after(int(1000 / 60), lambda: update(root, window))

def enable_jump():
    globals()['jump'] = True

def game():
    root, game_window = init()
    root.bind('<Key>', lambda e: enable_jump())

    root.after(int(1000 / 60), lambda: update(root, game_window))
    while True:
        root.update_idletasks()
        root.update()



def learn():
    root, game_window = init()

    model, env = load_custom_model(root, game_window)
    callback_on_best = StopTrainingOnRewardThreshold(reward_threshold=50000, verbose=1)
    eval_callback = EvalCallback(env, callback_on_new_best=callback_on_best, verbose=1)
    print('Learning start')

    model.learn(total_timesteps=1000000, tb_log_name='last', reset_num_timesteps=False, callback=eval_callback)

    PPO_Path = os.path.join('Training', 'Saved Models', 'Last')
    model.save(PPO_Path)
    del model
    model = chosen_algorithm.load(PPO_Path, env=env, verbose=verbose)

    print('please press space')


    render_test(model, env)
    # root.mainloop()

if sys.argv[1] == 'learn':
    learn()
elif sys.argv[1] == 'play':
    play_model()
elif sys.argv[1] == 'game':
    game()

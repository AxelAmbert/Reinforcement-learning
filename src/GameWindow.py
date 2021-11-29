import math
import sys
from tkinter import Canvas

import numpy as np
from PIL import Image, ImageTk, ImageOps

from src.GameInfo import GameInfo
from src.Pipe import Pipe
from src.Player import Player

# 60 FPS
from src.Point import Point
from src.Score import Score

TICK_DURATION = math.floor(1 / 60)

# 1,5 second
NEW_PIPE = 2000


class GameWindow(Canvas):

    def init_callbacks(self):
        self.player.jump()

    def update_player_pos(self):
        self.delete(self.crappy)
        self.crappy = self.player.draw(self)

    def update_pipes_pos(self):
        for pipe in self.pipes:
            pipe.tick()
            if pipe.is_out_of_bounds():
                self.pipes.remove(pipe)
            else:
                pipe.draw(self)

    def check_lose(self):
        results = self.find_overlapping(*self.player.get_hitbox())
        self.delete(self.hitbox_check)
        # self.hitbox_check = self.create_rectangle(*self.player.get_hitbox(), fill="red", tag="hitbox")

        if self.player.is_out_of_bounds():
            self.stop = True

        for result in results:
            if "pipe" in self.gettags(result):
                self.stop = True

    def update_pos(self):
        self.update_player_pos()
        self.update_pipes_pos()
        self.score.draw(self)

    def validate_pipe(self, pipe):
        if self.player.pos.x > pipe.positions[0].x:
            pipe.score_validated = True
            self.score.score += 1

    def check_score(self):
        for pipe in self.pipes:
            if pipe.score_validated:
                continue
            self.validate_pipe(pipe)

    def check_new_pipe(self):
        last_pipe = self.pipes[-1]

        if last_pipe.positions[0].x <= GameInfo.scree_size.x / 2:
            self.add_new_pipe()

    def get_distance_from_hole_pos(self):
        # print('pos {} - size {}'.format(self.pipes[-1].positions[0].y, self.pipes[-1].size.y))
        return int(self.pipes[-1].positions[0].y - self.pipes[-1].size.y / 2) - self.player.pos.y

    def get_distance_from_pipe(self):
        last_pipe = self.pipes[-1]
        pos = last_pipe.positions[0].x - self.player.pos.x

        return pos if pos >= 0 else 0

    def get_state(self):
        h_dist = self.get_distance_from_pipe()
        v_dist = self.get_distance_from_hole_pos()

        # print(h_dist, v_dist)

        return np.array([h_dist, v_dist])

    def tick(self, action):
        # if self.stop == False:
        #    self.after(TICK_DURATION, self.tick)

        self.update_pos()
        self.player.tick(action)
        self.check_lose()
        self.check_score()
        self.check_new_pipe()
        return self.get_state()
        # print('Y pos {} - Distance X {} - Y hole {}'.format(self.player.pos.y, self.get_distance_from_pipe(), self.get_pipe_hole_position()))

    def add_new_pipe(self):
        # self.after(NEW_PIPE, self.add_new_pipe)
        if self.player.started == False:
            return
        self.pipes.append(Pipe())

    def reset(self):

        for pipe in self.pipes:
            for tag in pipe.tags:
                self.delete(tag)
        self.score.score = 0
        self.pipes = [Pipe()]
        self.stop = False
        self.player = Player()

    def __init__(self, root):
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()

        super().__init__(width=480, height=640,
                         background="black", highlightthickness=0)
        self.screen_size = (480, 640)
        self.root = root
        self.player = Player()
        self.pack()
        self.pipes = [Pipe()]
        self.pipe_img = None
        self.flipped_pipe_img = None
        self.crappy = -1
        # Faire spawn les pipes sans time
        # self.after(NEW_PIPE, self.add_new_pipe)
        self.stop = False
        self.hitbox_check = None
        self.score = Score()
        self.i = 0

import math
import sys
from tkinter import Canvas
from PIL import Image, ImageTk, ImageOps

from src.GameInfo import GameInfo
from src.Pipe import Pipe
from src.Player import Player

# 60 FPS
from src.Point import Point
from src.Score import Score
import numpy as np

from src.Utils import Utils

TICK_DURATION = math.floor(1000 / 60)

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

    def draw_wanted(self):
        next_pipe_pos = self.pipes[-1].positions[1].y + self.pipes[-1].size.y / 2
        player_pos = self.player.get_player_pos()
        wanted_pos = next_pipe_pos + (GameInfo.window_size.y / 8) - self.player.size.y / 2

        self.delete(self.hitbox_check)
        start_x = self.pipes[-1].positions[1].x - self.pipes[-1].size.x / 2
        self.hitbox_check = self.create_rectangle(start_x, wanted_pos, start_x + self.player.size.x,
                                                  wanted_pos + self.player.size.y, fill="red", tag="hitbox")

    def check_lose(self):
        results = self.find_overlapping(*self.player.get_hitbox())
        # self.delete(self.hitbox_check)
        # self.hitbox_check = self.create_rectangle(*self.player.get_hitbox(), fill="red", tag="hitbox")

        if self.player.is_out_of_bounds():
            self.stop = True

        for result in results:
            if "pipe" in self.gettags(result):
                self.stop = True

    def update_pos(self):
        self.update_player_pos()
        self.update_pipes_pos()

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

        if last_pipe.positions[0].x <= 0:
            self.add_new_pipe()

    def get_pipe_hole_position(self):
        first_pipe_pos = Utils.clamp(int(self.pipes[-1].positions[1].y + self.pipes[-1].size.y / 2), 0, 640)
        second_pipe_pos = Utils.clamp(int(self.pipes[-1].positions[0].y - self.pipes[-1].size.y / 2), 0, 640)

        return [abs(first_pipe_pos - self.player.pos.y), abs(second_pipe_pos - self.player.pos.y)]

        # return [abs(first_pipe_pos - self.player.get_player_pos()), abs(second_pipe_pos - self.player.get_player_pos())]

        # return [self.clamp(first_pipe_pos, 0, 640), self.clamp(second_pipe_pos, 0, 640)]

    def get_distance_from_pipe(self):
        last_pipe = self.pipes[-1]
        pos = int(last_pipe.positions[0].x - last_pipe.size.x / 2) - int(self.player.pos.x + self.player.size.x / 2)

        return pos if pos >= 0 else 0

    def get_state(self):
        return np.array([
            self.get_distance_from_pipe(),
            *self.get_pipe_hole_position()])

    def tick(self, action):
        # if self.stop == False:
        #    self.after(TICK_DURATION, self.tick)
        self.player.tick(action)
        self.update_pos()
        self.check_lose()
        self.check_score()
        self.check_new_pipe()
        self.score.draw(self)
        self.draw_wanted()
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

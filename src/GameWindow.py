import math
import sys

import numpy as np
from PIL import Image, ImageTk, ImageOps
from pyglet.gl import glBegin, glEnd
from pyglet.graphics import Batch

from src.GameInfo import GameInfo
from src.Pipe import Pipe
from src.Player import Player

# 60 FPS
from src.Point import Point
from src.PygletUtils import PygletUtils
from src.Score import Score

TICK_DURATION = math.floor(1 / 60)

# 1,5 second
NEW_PIPE = 2000


class GameWindow:

    def init_callbacks(self):
        self.player.jump()

    def update_player_pos(self):
        self.player.draw()

    def update_pipes_pos(self):
        for pipe in self.pipes:
            if pipe.is_out_of_bounds():
                self.pipes.remove(pipe)
            else:
                pass
                # pipe.draw()



    def check_player_collide_pipe(self, pipe):
        last_pipe = pipe
        r1_x1, r1_x2, r1_y1, r1_y2 = PygletUtils.get_aabb(self.player.pos, self.player.size)

        for pipe_pos in last_pipe.positions:
            r2_x1, r2_x2, r2_y1, r2_y2 = PygletUtils.get_aabb(pipe_pos, last_pipe.size)

            #https://stackoverflow.com/a/23869476/9535211
            if not (r1_x1 > r2_x2 or r1_x2 < r2_x1 or r1_y1 > r2_y2 or r1_y2 < r2_y1):
                return True
        return False

    def check_lose(self):
        self.stop = self.player.is_out_of_bounds()

        for pipe in self.pipes:
            if self.check_player_collide_pipe(pipe):
                self.stop = True


    def update_pos(self):
        self.update_player_pos()
        self.update_pipes_pos()

    def validate_pipe(self, pipe):
        if self.player.pos.x > pipe.positions[0].x + pipe.size.x / 2:
            pipe.score_validated = True
            self.score.score += 1

    def check_score(self):
        for pipe in self.pipes:
            if pipe.score_validated:
                continue
            self.validate_pipe(pipe)

    def check_new_pipe(self):
        if self.get_distance_from_pipe() <= 0:
            self.add_new_pipe()

    def get_distance_from_pipe(self):
        last_pipe = self.pipes[-1]
        pos = last_pipe.positions[0].x + last_pipe.size.x - self.player.pos.x

        return pos if pos >= 0 else 0

    def get_state(self):
        last_pipe = self.pipes[-1]

        h_dist = self.get_distance_from_pipe()
        v_dist_one = self.player.pos.y + self.player.size.y / 2 - last_pipe.positions[0].y - last_pipe.size.y
        v_dist_two = self.player.pos.y + self.player.size.y / 2 - last_pipe.positions[1].y

        # print(np.array([h_dist, v_dist_one, v_dist_two]))
        # print(h_dist, v_dist)

        return np.array([h_dist, v_dist_one, v_dist_two])

    def draw_visualizer(self):
        state = self.get_state()
        next_pipe_pos = self.pipes[-1].positions[1].y + self.pipes[-1].size.y / 2
        player_pos = self.player.get_player_pos()
        wanted_pos = next_pipe_pos + (GameInfo.window_size.y / 4) - self.player.size.y / 2

        for draw_data in self.visualizer:
            self.delete(draw_data)
        self.visualizer.append(
            self.create_line(self.player.pos.x, self.player.pos.y, self.player.pos.x + state[0], self.player.pos.y,
                             fill="green"))
        self.visualizer.append(self.create_line(self.player.pos.x, self.player.pos.y, self.pipes[-1].positions[0].x,
                                                self.pipes[-1].positions[0].y - self.pipes[-1].size.y / 2, fill="red"))
        self.visualizer.append(self.create_line(self.player.pos.x, self.player.pos.y, self.pipes[-1].positions[0].x,
                                                self.pipes[-1].positions[1].y + self.pipes[-1].size.y / 2,
                                                fill="white"))
        # print('{} - {}'.format(self.player.pos.y + state[1], self.player.pos.y + state[2]) )

    def pipes_tick(self):
        for pipe in self.pipes:
            pipe.tick()

    def tick(self, action):

        self.pipes_tick()
        self.player.tick(action)
        self.check_lose()
        self.check_score()
        self.check_new_pipe()
        # self.draw_visualizer()

        return self.get_state()
        # print('Y pos {} - Distance X {} - Y hole {}'.format(self.player.pos.y, self.get_distance_from_pipe(), self.get_pipe_hole_position()))

    def draw(self):
        self.update_pos()
        for pipe in self.pipes:
            pipe.draw()
        self.batch.draw()
        self.score.draw()


    def add_new_pipe(self):
        # self.after(NEW_PIPE, self.add_new_pipe)
        if self.player.started == False:
            return
        self.pipes.append(Pipe(self.batch))

    def reset(self):
        self.batch = Batch()
        self.score.score = 0
        self.pipes = [Pipe(self.batch)]
        self.stop = False
        self.player = Player(self.batch)

    def __init__(self):
        self.batch = Batch()
        self.player = Player(self.batch)
        self.pipes = [Pipe(self.batch)]
        self.pipe_img = None
        self.flipped_pipe_img = None
        self.crappy = -1
        # Faire spawn les pipes sans time
        # self.after(NEW_PIPE, self.add_new_pipe)
        self.stop = False
        self.hitbox_check = None
        self.hitbox_pipes = None
        self.score = Score()
        self.visualizer = []
        self.i = 0

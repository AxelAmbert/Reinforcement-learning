import math
import sys
from tkinter import Canvas
from PIL import Image, ImageTk, ImageOps

from src.Pipe import Pipe
from src.Player import Player

# 60 FPS
from src.Point import Point

TICK_DURATION = math.floor(1000 / 60)

# 1 second
NEW_PIPE = 2000


class GameWindow(Canvas):

    def mdr(self):
        print('lol')

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
        #self.hitbox_check = self.create_rectangle(*self.player.get_hitbox(), fill="red", tag="hitbox")

        for result in results:
            if "pipe" in self.gettags(result):
                self.stop = True

    def update_pos(self):
        self.update_player_pos()
        self.update_pipes_pos()

    def tick(self):
        self.update_pos()
        self.player.tick()
        self.check_lose()
        if self.stop == False:
            self.after(TICK_DURATION, self.tick)

    def add_new_pipe(self):
        if self.player.started == False:
            return
        self.pipes.append(Pipe())
        self.after(NEW_PIPE, self.add_new_pipe)

    def __init__(self, root):
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()

        super().__init__(width=480, height=640,
                         background="black", highlightthickness=0)
        self.root = root
        self.player = Player()
        self.pack()
        self.pipes = []
        self.pipe_img = None
        self.flipped_pipe_img = None
        self.crappy = -1
        self.after(NEW_PIPE, self.add_new_pipe)
        self.stop = False
        self.hitbox_check = None
        self.tick()

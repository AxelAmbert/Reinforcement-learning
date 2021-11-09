import math
from tkinter import Canvas
from PIL import Image, ImageTk, ImageOps

from src.Pipe import Pipe
from src.Player import Player

# 60 FPS
from src.Point import Point

TICK_DURATION = math.floor(1000 / 60)

# 1 second
NEW_PIPE = 2500

class GameWindow(Canvas):

    def mdr(self):
        print('lol')

    def init_callbacks(self):
        self.player.jump()

    def update_player_pos(self):
        self.delete(self.crappy)
        self.crappy = self.create_image(self.player.pos.x, self.player.pos.y, image=self.crappy_img)


    def update_pipes_pos(self):
        for pipe in self.pipes:
            pipe.tick()
            if pipe.tag is not None:
                self.delete(pipe.tag)
            if pipe.pos.x <= -pipe.size.x:
                self.pipes.remove(pipe)
            else:
                pipe.tag = self.create_image(pipe.pos.x, pipe.pos.y, image=
                self.flipped_pipe_img if pipe.flipped is True else self.pipe_img, tag='pipe')

    def check_lose(self):
        results = self.find_overlapping(self.player.pos.x, self.player.pos.y, self.player.pos.x + self.player.size.x, self.player.pos.y + self.player.size.y)

        for result in results:
            if "pipe" in self.gettags(result):
                print('lose')



    def update_pos(self):
        self.update_player_pos()
        self.update_pipes_pos()

    def tick(self):
        self.update_pos()
        self.player.tick()
        self.check_lose()
        self.after(TICK_DURATION, self.tick)


    def add_new_pipe(self):
        self.pipes.append(Pipe(Point(self.root.winfo_screenwidth(), self.root.winfo_screenheight())))
        self.after(NEW_PIPE, self.add_new_pipe)

    def init_image(self):
        tmp_pipe_img = Image.open("./resources/pipe2.png").convert("RGBA")
        im_flip = ImageOps.flip(tmp_pipe_img)

        self.pipe_img = ImageTk.PhotoImage(tmp_pipe_img)
        self.flipped_pipe_img = ImageTk.PhotoImage(im_flip)

    def __init__(self, root):
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()

        super().__init__(width=500, height=500,
                         background="black", highlightthickness=0)
        self.root = root
        self.player = Player()
        self.pack()
        self.init_callbacks()
        self.crappy_img = ImageTk.PhotoImage(Image.open("./resources/crappy_bird.png").convert("RGBA"))
        self.crappy = self.create_image(self.player.pos.x, self.player.pos.y, image=self.crappy_img)
        self.pipes = []
        self.pipe_img = None
        self.flipped_pipe_img = None
        self.init_image()
        self.after(NEW_PIPE, self.add_new_pipe)
        self.tick()

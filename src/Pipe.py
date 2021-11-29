from functools import cached_property

from PIL import Image, ImageTk, ImageOps

from src.GameInfo import GameInfo
from src.Point import Point
import random

done = True

class Pipe:


    def draw(self, canvas):
        for tag in self.tags:
            canvas.delete(tag)

        self.tags[0] = canvas.create_image(self.positions[0].x, self.positions[0].y, tag='pipe', image=self.pipe_img)
        self.tags[1] = canvas.create_image(self.positions[1].x, self.positions[1].y, tag='pipe', image=self.flipped_pipe_img)

    @cached_property
    def init_images(self):
        tmp_pipe_img = Image.open("./resources/coolpipe.png").convert("RGBA").resize((self.size.x, self.size.y))
        im_flip = ImageOps.flip(tmp_pipe_img)

        pipe_img = ImageTk.PhotoImage(tmp_pipe_img)
        flipped_pipe_img = ImageTk.PhotoImage(im_flip)
        return pipe_img, flipped_pipe_img

    def init_positions(self):
        # Let a space of about 1/4 of the screen to go throught, and a margin of 10% because the pipe should
        # not be stuck to the ground
        go_through = GameInfo.window_size.y / 4
        max_size = int(GameInfo.window_size.y - go_through - GameInfo.window_size.y / 10)
        rdm_size = random.randint(int(GameInfo.window_size.y / 7), max_size)
        first_pipe_size = GameInfo.window_size.y - rdm_size
        second_pipe_size = first_pipe_size - go_through

        first_pipe = Point(GameInfo.window_size.x + self.size.x / 2, first_pipe_size + self.size.y / 2)
        second_pipe = Point(GameInfo.window_size.x + self.size.x / 2, second_pipe_size - self.size.y / 2)

        return [first_pipe, second_pipe]

    def is_out_of_bounds(self):
        return self.positions[0].x <= 0 - self.size.x

    def __init__(self):
        r = random.randint(0, 1)
        self.size = Point(GameInfo.window_size.x / 6, GameInfo.window_size.y)
        self.positions = self.init_positions()
        self.tags = [None, None]
        self.flipped = True if r == 0 else False
        self.pipe_img, self.flipped_pipe_img = self.init_images
        self.score_validated = False

    def tick(self):
        for pos in self.positions:
            pos.x -= 5

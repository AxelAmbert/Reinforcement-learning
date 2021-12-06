import sys
from functools import cached_property

from pyglet import image
from pyglet.image import ImageData
from pyglet.sprite import Sprite

from src.GameInfo import GameInfo
from src.Point import Point
import random

from src.PygletUtils import PygletUtils

done = True

class Pipe:

    i = 0
    def draw(self,):
        self.pipe_sprite.update(self.positions[0].x, self.positions[0].y)
        self.flipped_pipe_sprite.update(self.positions[1].x, self.positions[1].y)
        #self.pipe_img.blit(self.positions[0].x, self.positions[0].y)
        #self.flipped_pipe_img.blit(self.positions[1].x, self.positions[1].y)
        #self.tags[0] = canvas.create_image(self.positions[0].x, self.positions[0].y, tag='pipe', image=self.pipe_img)
        #self.tags[1] = canvas.create_image(self.positions[1].x, self.positions[1].y, tag='pipe', image=self.flipped_pipe_img)

    @cached_property
    def init_images(self):
        pipe_img = image.load("./resources/coolpipe.png")
        PygletUtils.image_scale(pipe_img, self.size.x, self.size.y)
        flipped_pipe_img = image.load("./resources/coolpipeflip.png")
        PygletUtils.image_scale(flipped_pipe_img, self.size.x, self.size.y)

        return pipe_img, flipped_pipe_img

    def init_sprites(self):
        pipe_sprite = Sprite(self.pipe_img, self.positions[0].x, self.positions[0].y, batch=self.batch)
        flipped_pipe_sprite = Sprite(self.flipped_pipe_img, self.positions[1].x, self.positions[1].y, batch=self.batch)

        return pipe_sprite, flipped_pipe_sprite

    def init_positions(self):
        # Let a space of about 1/4 of the screen to go throught, and a margin of 10% because the pipe should
        # not be stuck to the ground
        go_through = GameInfo.window_size.y / 4
        max_size = int(GameInfo.window_size.y - go_through - GameInfo.window_size.y / 10)
        rdm_size = random.randint(int(GameInfo.window_size.y / 7), max_size)
        first_pipe_size = -GameInfo.window_size.y + rdm_size
        second_pipe_size = first_pipe_size + go_through + GameInfo.window_size.y
        #print('rdm {} - {}'.format(rdm_size, first_pipe_size))

        first_pipe = Point(GameInfo.window_size.x + self.size.x, first_pipe_size)
        second_pipe = Point(GameInfo.window_size.x + self.size.x, second_pipe_size)

        return [first_pipe, second_pipe]

    def is_out_of_bounds(self):
        return self.positions[0].x + self.size.x <= 0

    def __init__(self, batch):
        self.batch = batch
        self.size = Point(GameInfo.window_size.x / 6, GameInfo.window_size.y)
        self.positions = self.init_positions()
        self.tags = [None, None]
        self.pipe_img, self.flipped_pipe_img = self.init_images
        self.pipe_sprite, self.flipped_pipe_sprite = self.init_sprites()
        self.score_validated = False

    def tick(self):
        for pos in self.positions:
            pos.x -= 5

    def get_hitbox(self, index):
        start_x = self.positions[index].x  # + self.adjust_hitbox()
        start_y = self.positions[index].y
        end_x = self.positions[index].x + self.size.x  # + self.adjust_hitbox()
        end_y = self.positions[index].y + self.size.y  # - self.adjust_hitbox()

        return [start_x, start_y, end_x, end_y]

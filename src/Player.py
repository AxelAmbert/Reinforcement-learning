from PIL import ImageTk
from PIL import Image
from pyglet import image
from pyglet.image.codecs.png import PNGImageDecoder
from pyglet.sprite import Sprite

from Point import Point
from src.GameInfo import GameInfo
from src.PygletUtils import PygletUtils
JUMP = 1

class Player:

    def clamp(self, value, min, max):
        return min if value < min else value if value < max else max

    def init_player_img(self):
        self.player_img = PygletUtils.create_image_rgba("./resources/crappy_bird.png")
        self.player_sprite = Sprite(self.player_img, self.pos.x, self.pos.y, batch=self.batch)
        PygletUtils.image_scale(self.player_img, self.size.x, self.size.y)

    def __init__(self, batch):
        self.size = Point(54 * (GameInfo.window_size.x / 480), 40 * (GameInfo.window_size.y / 640))
        self.pos = Point(250, 250)
        self.player_sprite = None
        self.batch = batch
        self.started = GameInfo.is_AI
        self.is_flying = False
        self.tick_count = 0
        self.fall_count = 0
        self.player_img = None
        self.show_img = None
        self.init_player_img()
        self.velocity = -1
        self.min_velocity = -10

    def update_player_img(self):

        rotated = self.player_img.rotate(0 - (self.velocity * 3))
        '''if self.is_flying:
            rotated = self.player_img.rotate(self.tick_count * 6, expand=True)
        else:
            rotated = self.player_img.rotate(self.clamp(self.fall_count, 0, 10) * -4.5, expand=True)'''
        #rotated = self.player_img
        self.show_img = ImageTk.PhotoImage(rotated)

    def draw(self):
        self.player_sprite.update(self.pos.x, self.pos.y)

    def tick(self, action):
        if action == JUMP:
            self.velocity = 17
            self.jump()
        if self.velocity > self.min_velocity:
            self.velocity -= 2
        self.pos.y += self.velocity

    def jump(self):
        self.is_flying = True
        self.started = True

    def is_out_of_bounds(self):
        return self.pos.y + self.size.y <= 0 or self.pos.y > GameInfo.window_size.y

    def adjust_hitbox(self):
        if self.is_flying:
            return (self.size.x / 50) * self.tick_count * 2

        return self.clamp(self.fall_count, 0, 10) * self.size.x / 50

    def get_clamped_pos(self):
        pos = int(self.pos.y - self.size.y / 2)

        return self.clamp(pos, 0, 640)

    def get_player_pos(self):
        return int(self.pos.y - self.size.y / 2)

    def get_hitbox(self):
        start_x = self.pos.x #+ self.adjust_hitbox()
        start_y = self.pos.y
        end_x = self.pos.x + self.size.x# + self.adjust_hitbox()
        end_y = self.pos.y + self.size.y#- self.adjust_hitbox()

        return [start_x, start_y, end_x, end_y,]
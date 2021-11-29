from PIL import ImageTk
from PIL import Image

from Point import Point
from src.GameInfo import GameInfo
from Utils import *

JUMP = 1

class Player:


    def init_player_img(self):
        self.player_img = Image.open("./resources/crappy_bird.png").convert("RGBA").resize((self.size.x, self.size.y))

    def __init__(self):
        self.size = Point(54 * (GameInfo.window_size.x / 480), 40 * (GameInfo.window_size.y / 640))
        self.pos = Point(100, 250)

        self.started = GameInfo.is_AI
        self.is_flying = False
        self.tick_count = 0
        self.fall_count = 0
        self.player_img = None
        self.show_img = None
        self.init_player_img()

    def update_player_img(self):

        if self.is_flying:
            rotated = self.player_img.rotate(self.tick_count * 6, expand=True)
        else:
            rotated = self.player_img.rotate(Utils.clamp(self.fall_count, 0, 10) * -4.5, expand=True)
        #rotated = self.player_img
        self.show_img = ImageTk.PhotoImage(rotated)

    def draw(self, canvas):
        self.update_player_img()
        return canvas.create_image(self.pos.x, self.pos.y, image=self.show_img, tag="player")

    def tick(self, action):

        self.is_flying = action == JUMP
        if action == JUMP:
            self.pos.y -= 10
        else:
            self.pos.y += 10
            '''
            self.fall_count += 1
            self.tick_count = 0
            self.is_flying = False
            if self.fall_count >= 5:
                self.pos.y += 8'''
           # self.jump()
        '''if self.is_flying and self.tick_count < 5:
            self.tick_count += 1
            self.pos.y -= 15
            self.fall_count = 0'''

    def jump(self):
        self.is_flying = True
        self.started = True

    def get_player_pos(self):
        return int(self.pos.y - self.size.y / 2)

    def is_out_of_bounds(self):
        return self.get_player_pos() <= 0 or int(self.pos.y + self.size.y / 2) >= GameInfo.window_size.y

    def adjust_hitbox(self):
        if self.is_flying:
            return (self.size.x / 50) * self.tick_count * 2

        return self.clamp(self.fall_count, 0, 10) * self.size.x / 50

    def get_clamped_pos(self):
        pos = int(self.pos.y - self.size.y / 2)

        return self.clamp(pos, 0, 640)

    def get_hitbox(self):
        start_x = self.pos.x - self.size.x / 2 #+ 50 #+ self.adjust_hitbox()
        start_y = self.pos.y - self.size.y / 2 #+ 50
        end_x = self.pos.x + self.size.x - self.size.x / 2 #- 50# + self.adjust_hitbox()
        end_y = self.pos.y + self.size.y - self.size.y / 2 #- 50#- self.adjust_hitbox()

        return [start_x, start_y, end_x, end_y,]
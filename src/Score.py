import pyglet
from src.GameInfo import GameInfo


class Score:

    def draw(self):

        if self.score != self.last_score:
            self.last_score = self.score
            self.label.text = str(self.score)
        self.label.draw()
        pass#self.score_tag = canvas.create_text(GameInfo.window_size.x / 2, 50, text=str(self.score), fill="white")

    def __init__(self):
        self.score = 0
        self.last_score = 0
        self.label = pyglet.text.Label('0',
                          font_name='Times New Roman',
                          font_size=25,
                          x=GameInfo.window_size.x // 2, y=GameInfo.window_size.y - 50,
                          anchor_x='center', anchor_y='center')


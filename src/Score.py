from src.GameInfo import GameInfo


class Score:

    def draw(self, canvas):
        canvas.delete(self.score_tag)
        self.score_tag = canvas.create_text(GameInfo.window_size.x / 2, 50, text=str(self.score), fill="white")

    def __init__(self):
        self.score = 0
        self.score_tag = -1

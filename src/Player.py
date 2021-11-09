from Point import Point


class Player:

    def __init__(self):
        self.pos = Point(50, 500)
        self.size = Point(0, 0)
        self.is_flying = False
        self.tick_count = 0
        pass

    def tick(self):
        if self.is_flying and self.tick_count < 3:
            self.tick_count += 1
            self.pos.y -= 20
        else:
            self.tick_count = 0
            self.is_flying = False
            self.pos.y += 1

    def jump(self):
        if self.pos.y + self.size.y - 20 > 0:
            self.is_flying = True

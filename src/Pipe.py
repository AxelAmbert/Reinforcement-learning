from src.Point import Point
import random


class Pipe:

    def __init__(self, size):
        r = random.randint(0, 1)
        rdm_pos = [Point(500, 100), Point(500, 400)]

        self.pos = rdm_pos[r]
        self.size = Point(100, 200)
        self.tag = None
        self.flipped = True if r == 0 else False

    def tick(self):
        self.pos.x -= 2

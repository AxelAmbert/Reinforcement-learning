class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __call__(self):
        print("Point(x={}, y={})".format(self.x, self.y))

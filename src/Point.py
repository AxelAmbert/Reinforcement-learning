class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return "Point(x={}, y={})".format(self.x, self.y)
    def __call__(self):
        print("Point(x={}, y={})".format(self.x, self.y))

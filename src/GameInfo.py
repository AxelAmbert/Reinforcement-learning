from src.Point import Point


class GameInfo:
    scree_size = Point(0, 0)
    window_size = Point(0, 0)

    @staticmethod
    def init_size(root):
        width, heigth = root.winfo_screenwidth(),  root.winfo_screenheight()
        GameInfo.screen_size = Point(width, heigth)

        # On a 1920x1080 screen it is very close to a 480x640 ratio, like the original game
        GameInfo.window_size = Point(GameInfo.screen_size.x / 4, GameInfo.screen_size.y / 1.70)

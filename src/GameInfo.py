from src.Point import Point


class GameInfo:
    scree_size = Point(0, 0)
    window_size = Point(0, 0)
    is_AI = False

    @staticmethod
    def init_info(size, AI):

        # On a 1920x1080 screen it is very close to a 480x640 ratio, like the original game
        #GameInfo.window_size = Point(GameInfo.screen_size.x / 4, GameInfo.screen_size.y / 1.70)
        GameInfo.window_size = size
        GameInfo.is_AI = AI


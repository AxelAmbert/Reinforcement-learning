class Utils:
    @staticmethod
    def clamp(value, minimum, maximum):
        return minimum if value < minimum else value if value < maximum else maximum
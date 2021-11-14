from tkinter import *

from src.GameInfo import GameInfo
from src.MainWindow import GameWindow

root = Tk()

root.title("Welcome to LikeGeeks app")
GameInfo.init_size(root)

game_window = GameWindow(root)

root.bind('<Key>', lambda e: game_window.init_callbacks())

root.mainloop()

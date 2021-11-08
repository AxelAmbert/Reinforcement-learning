from tkinter import Canvas


class GameWindow:

    def __init__(self, root):
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        self.window = Canvas(root, width=width / 4, height=height / 4, bg="black")
        self.window.create_oval(0, 0, 50, 50, fill="magenta")
        self.window.pack()

from tkinter import Tk
from tkinter import ttk

from strings import en as STRINGS

class BasePage:
    def __init__(self):
        self.root = Tk()
        self.root.title(STRINGS.APP_TITLE)
        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.grid()

        self.render() 

    def render(self):
        pass

    def run(self):
        self.root.mainloop()

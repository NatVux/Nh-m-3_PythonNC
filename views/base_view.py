import tkinter as tk
from constants import COLORS

class BaseView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['background'])
        self.parent = parent
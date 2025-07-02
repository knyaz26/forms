import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, win):
        self.win = win
        self.win.title("Dashboard")
        self.win.state('zoomed')
        self.win.configure(background='#303030')
        self.frame = ttk.Frame(self.win)
        self.frame.pack(fill='y', expand=True, padx=10, pady=10)

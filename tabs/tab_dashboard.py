from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TabDashboard():
    def __init__(self):
        pass

    def enter(self, parent):
        self.label_title = ttk.Label(parent, text="tab dashboard", font=("Arial", 24))
        self.label_title.pack(padx=20, pady=20)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.axs = self.fig.subplots(2, 2)

        self.axs[0, 0].plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro-')
        self.axs[0, 1].plot([1, 2, 3, 4], [1, 2, 3, 4], 'bo-')
        self.axs[1, 0].plot([1, 2, 3, 4], [1, 3, 2, 4], 'go-')
        self.axs[1, 1].plot([1, 2, 3, 4], [1, 2, 4, 3], 'yo-')

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    def exit(self):
        for widget in getattr(self, "parent", tk.Frame()).winfo_children():
            widget.pack_forget()


tab_dashboard = TabDashboard()
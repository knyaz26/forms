from tkinter import ttk

class TabDashboard():
    def __init__(self):
        pass

    def enter(self, parent):
        self.test = ttk.Label(parent, text="tab dashboard", font=("Arial", 24))
        self.test.pack(padx=20, pady=20)

    def exit(self):
        self.test.pack_forget()


tab_dashboard = TabDashboard()
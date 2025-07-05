from tkinter import ttk
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import supabase as sb

class TabDashboard():
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.db = sb.create_client(self.url, self.key)

    def get_doctor_chart_data(self):
        chart_data = {}
        result = self.db.table("hx_1023").select("doctor").execute()
        rows = getattr(result, "data", [])
        doctors = set()
        for row in rows:
            doctor = row.get("doctor", "")
            if doctor and doctor.strip():
                doctors.add(doctor.strip())
        distinct_doctors = list(doctors)
        for i in distinct_doctors:
            res = self.db.table("hx_1023").select("doctor", count="exact").eq("doctor", i).execute()
            count = res.count
            chart_data[i] = count
        return chart_data

    def enter(self, parent):
        chart_data = self.get_doctor_chart_data()
        self.label_title = ttk.Label(parent, text="tab dashboard", font=("Arial", 24))
        self.label_title.pack(padx=20, pady=20)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.axs = self.fig.subplots(2, 2)

        self.axs[0, 0].pie(list(chart_data.values()), labels=list(chart_data.keys()))
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
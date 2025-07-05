from tkinter import ttk
import tkinter as tk
from matplotlib import pyplot as plt
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

    def get_allergies_data(self):
        allergies_data = {}
        result = self.db.table("alg_450").select("allergies").execute()
        rows = getattr(result, "data", [])
        for row in rows:
            allergies = row.get("allergies", [])
            if allergies:
                for allergy in allergies:
                    cleaned = allergy.strip()
                    if cleaned:
                        allergies_data[cleaned] = allergies_data.get(cleaned, 0) + 1
        return allergies_data


    def enter(self, parent):
        chart_data = self.get_doctor_chart_data()
        allergies_data = self.get_allergies_data()
        self.label_title = ttk.Label(parent, text="tab dashboard", font=("Arial", 24))
        self.label_title.pack(padx=20, pady=20)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        plt.style.use('dark_background')
        self.fig.patch.set_facecolor('#222222')
        self.axs = self.fig.subplots(2, 2)

        self.axs[0, 0].pie(list(chart_data.values()), labels=list(chart_data.keys()))
        self.axs[0, 1].stem(list(allergies_data.values()), label=list(allergies_data.keys()), markerfmt="o", basefmt=" ")
        self.axs[1, 0].plot([1, 2, 3, 4], [1, 3, 2, 4], 'go-')
        self.axs[1, 1].plot([1, 2, 3, 4], [1, 2, 4, 3], 'yo-')

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    def exit(self):
        for widget in getattr(self, "parent", tk.Frame()).winfo_children():
            widget.pack_forget()


tab_dashboard = TabDashboard()
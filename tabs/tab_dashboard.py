import random
from tkinter import ttk
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.dates import DayLocator
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

    def get_date_data(self):
        date_data = {}
        dates = []
        result = self.db.table("hx_1023").select("date").execute()
        rows = getattr(result, "data", [])
        for row in rows:
            date = row.get("date")
            date = date.split("/")
            if date[2] == "2025":
                dates.append(date[1])
        for date in dates:
            if date not in date_data:
                date_data[date] = 1
            else:
                date_data[date] += 1
        return dict(sorted(date_data.items()))

    def enter(self, parent):
        chart_data = self.get_doctor_chart_data()
        allergies_data = self.get_allergies_data()
        date_data = self.get_date_data()
        self.label_title = ttk.Label(parent, text="tab dashboard", font=("Arial", 24))
        self.label_title.pack(padx=20, pady=20)
        a = []
        b = []
        for i in range(20):
            a.append(random.randint(1, 100))
            b.append(random.randint(1, 100))

        self.fig = Figure(figsize=(5, 4), dpi=100)
        plt.style.use('dark_background')
        self.fig.patch.set_facecolor('#222222')
        self.axs = self.fig.subplots(2, 2)

        self.axs[0, 0].pie(list(chart_data.values()), labels=list(chart_data.keys()))
        self.axs[0, 1].stem(list(allergies_data.values()), label=list(allergies_data.keys()), markerfmt="o", basefmt=" ")
        self.axs[1, 0].fill_between(list(date_data.keys()), list(date_data.values()), color='orange')
        self.axs[1, 0].tick_params(axis='x', rotation=45, labelsize=8)
        self.axs[1, 1].scatter(a, b ,color='red')

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    def exit(self):
        for widget in getattr(self, "parent", tk.Frame()).winfo_children():
            widget.pack_forget()


tab_dashboard = TabDashboard()

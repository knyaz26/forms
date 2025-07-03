import tkinter as tk
from tkinter import ttk

from tabs.tab_dashboard import tab_dashboard
from tabs.tab_hx_1023 import tab_hx_1023
from tabs.tab_alg_459 import tab_alg_450

class Dashboard:
    def __init__(self, win):
        self.win = win
        self.current_tab = tab_dashboard
        self.tabs = {
            'dashboard': tab_dashboard,
            'hx_1023': tab_hx_1023,
            'alg_450': tab_alg_450,
        }
        self.window_setup()
        self.side_bar_setup()
        self.main_frame_setup()


    def window_setup(self):
        self.win.title("forms")
        self.win.state('zoomed')
        self.win.configure(background='#303030')
       
    def side_bar_setup(self):
        self.side_bar = ttk.Frame(self.win)
        self.side_bar.pack(side='left', fill='y', padx=10, pady=10)

        self.label_app_name = ttk.Label(self.side_bar, text="FORMS", font=("Arial", 30), width=10)
        self.label_app_name.pack(padx=10, pady=10, anchor='w')

        # display
        self.frame_display = ttk.Frame(self.side_bar)
        self.frame_display.pack(fill='x', padx=10, pady=10)
        self.label_display = ttk.Label(self.frame_display, text="Display", font=("Arial", 14))
        self.label_display.pack(anchor='w', padx=5, pady=5)
        self.button_dashboard = ttk.Button(self.frame_display, text="Dashboard", command=self.on_button_dashboard_clicked)
        self.button_dashboard.pack(fill='x', anchor='w', padx=3, pady=3)
        self.button_spreadsheet = ttk.Button(self.frame_display, text="Spreadsheet", command=self.on_button_spreadsheet_clicked)
        self.button_spreadsheet.pack(fill='x', anchor='w', padx=3, pady=3)

        # insert
        self.frame_insert = ttk.Frame(self.side_bar)
        self.frame_insert.pack(fill='x', padx=10, pady=10)
        self.label_insert = ttk.Label(self.frame_insert, text="Insert", font=("Arial", 14))
        self.label_insert.pack(anchor='w', padx=5, pady=5)
        self.button_HX_1023 = ttk.Button(self.frame_insert, text="HX-1023", command=self.on_button_hx_1023_clicked)
        self.button_HX_1023.pack(fill='x', anchor='w', padx=3, pady=3)
        self.button_ALG_450 = ttk.Button(self.frame_insert, text="ALG-450", command=self.on_button_alg_450_clicked)
        self.button_ALG_450.pack(fill='x', anchor='w', padx=3, pady=3)

        # export
        self.frame_export = ttk.Frame(self.side_bar)
        self.frame_export.pack(fill='x', padx=10, pady=10)
        self.label_export = ttk.Label(self.frame_export, text="Export", font=("Arial", 14))
        self.label_export.pack(anchor='w', padx=5, pady=5)
        self.button_pdf = ttk.Button(self.frame_export, text="Export PDF", command=self.on_button_pdf_clicked)
        self.button_pdf.pack(fill='x', anchor='w', padx=3, pady=3)
        self.button_xlsx = ttk.Button(self.frame_export, text="Export XLSX", command=self.on_button_xlsx_clicked)
        self.button_xlsx.pack(fill='x', anchor='w', padx=3, pady=3)

    def main_frame_setup(self):
        self.main_frame = ttk.Frame(self.win)
        self.main_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        self.current_tab.enter(self.main_frame)


    def on_button_dashboard_clicked(self):
        self.current_tab.exit()
        self.current_tab = self.tabs['dashboard']
        self.current_tab.enter(self.main_frame)

    def on_button_spreadsheet_clicked(self):
        pass

    def on_button_hx_1023_clicked(self):
        self.current_tab.exit()
        self.current_tab = self.tabs['hx_1023']
        self.current_tab.enter(self.main_frame)

    def on_button_alg_450_clicked(self):
        self.current_tab.exit()
        self.current_tab = self.tabs['alg_450']
        self.current_tab.enter(self.main_frame)

    def on_button_pdf_clicked(self):
        pass

    def on_button_xlsx_clicked(self):
        pass

import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, win):
        self.win = win
        self.window_setup()
        self.side_bar_setup()

    def window_setup(self):
        self.win.title("forms")
        self.win.state('zoomed')
        self.win.configure(background='#303030')
       
    def side_bar_setup(self):
        self.side_bar = ttk.Frame(self.win)
        self.side_bar.pack(anchor='w', fill='y', expand=True, padx=10, pady=10)

        self.label_app_name = ttk.Label(self.side_bar, text="FORMS", font=("Arial", 30))
        self.label_app_name.pack(padx=10, pady=10)

        #display
        self.frame_display = ttk.Frame(self.side_bar)
        self.frame_display.pack(padx=10, pady=10, fill='x')

        self.button_dashboard = ttk.Button(self.frame_display, text="Dashboard", command=self.on_button_dashboard_clicked)
        self.button_dashboard.pack()
        self.button_spreadsheet = ttk.Button(self.frame_display, text="Spreadsheet", command=self.on_button_spreadsheet_clicked)
        self.button_spreadsheet.pack()

        #input
        self.frame_insert = ttk.Frame(self.side_bar)
        self.frame_insert.pack(padx=10, pady=10, fill='x')

        self.button_HX_1023 = ttk.Button(self.frame_insert, text="HX-1023", command=self.on_button_hx_1023_clicked)
        self.button_HX_1023.pack()

        self.button_ALG_450 = ttk.Button(self.frame_insert, text="ALG-450", command=self.on_button_alg_450_clicked)
        self.button_ALG_450.pack()

        #export
        self.frame_export = ttk.Frame(self.side_bar)
        self.frame_export.pack(padx=10, pady=10, fill='x')

        self.button_pdf = ttk.Button(self.frame_export, text="Export PDF", command=self.on_button_pdf_clicked)
        self.button_pdf.pack()

        self.button_xlsx = ttk.Button(self.frame_export, text="Export XLSX", command=self.on_button_xlsx_clicked)
        self.button_xlsx.pack()

    def on_button_dashboard_clicked(self):
        pass

    def on_button_spreadsheet_clicked(self):
        pass

    def on_button_hx_1023_clicked(self):
        pass

    def on_button_alg_450_clicked(self):
        pass

    def on_button_pdf_clicked(self):
        pass

    def on_button_xlsx_clicked(self):
        pass

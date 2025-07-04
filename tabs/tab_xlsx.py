from tkinter import ttk, filedialog
import tkinter as tk
from dotenv import load_dotenv
import os
import supabase as sb
import pandas as pd

load_dotenv()

class TabXLSX():
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.db = sb.create_client(self.url, self.key)
        self.tables = [("ALG-450", "alg_450"), ("HX-1023", "hx_1023")]

    def enter(self, parent):
        self.parent = parent
        self.label_instructions = ttk.Label(parent, text="Select document type and export the entire table as Excel.", font=("Arial", 14))
        self.label_instructions.pack(padx=10, pady=10)

        self.frame_select = ttk.Frame(parent)
        self.frame_select.pack(padx=10, pady=5, fill='x')

        self.label_doc_type = ttk.Label(self.frame_select, text="Document type:", font=("Arial", 12))
        self.label_doc_type.pack(side='left', padx=5)
        self.doc_type_var = tk.StringVar(value=self.tables[0][1])
        self.combo_doc_type = ttk.Combobox(self.frame_select, textvariable=self.doc_type_var, state="readonly")
        self.combo_doc_type['values'] = [t[0] for t in self.tables]
        self.combo_doc_type.current(0)
        self.combo_doc_type.pack(side='left', padx=5)

        self.button_generate = ttk.Button(parent, text="Export as Excel", command=self.on_generate_xlsx)
        self.button_generate.pack(padx=10, pady=15)

        self.label_status = ttk.Label(parent, text="", font=("Arial", 11))
        self.label_status.pack(padx=10, pady=5)

    def on_generate_xlsx(self):
        doc_type_idx = self.combo_doc_type.current()
        table_name = self.tables[doc_type_idx][1]

        data = self.db.table(table_name).select("*").execute()
        rows = getattr(data, "data", [])
        if not rows:
            self.label_status.config(text="No data found in this table.", foreground="red")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Excel as"
        )
        if not file_path:
            self.label_status.config(text="Excel export cancelled.", foreground="orange")
            return

        try:
            df = pd.DataFrame(rows)
            df.to_excel(file_path, index=False, engine='xlsxwriter')
            self.label_status.config(text=f"Excel saved to {file_path}", foreground="green")
        except Exception as e:
            self.label_status.config(text=f"Error: {e}", foreground="red")

    def exit(self):
        for widget in getattr(self, "parent", tk.Frame()).winfo_children():
            widget.pack_forget()

tab_xlsx = TabXLSX()

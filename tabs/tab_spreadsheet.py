from tkinter import ttk
from dotenv import load_dotenv
import os
import tkinter as tk
import supabase as sb

load_dotenv()

class TabSpreadsheet:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.db = sb.create_client(self.url, self.key)
        self.tables = ["hx_1023", "alg_450"]

    def enter(self, parent):
        self.parent = parent
        self.trees = []
        for widget in parent.winfo_children():
            widget.destroy()

        for table in self.tables:
            ttk.Label(parent, text=table, font=("Arial", 18)).pack(padx=10, pady=(20, 5), anchor='w')
            data = self.db.table(table).select("*").execute()
            rows = getattr(data, "data", [])
            if not rows:
                ttk.Label(parent, text="No data.", font=("Arial", 12)).pack(padx=10, pady=5, anchor='w')
                continue
            columns = list(rows[0].keys())
            tree = ttk.Treeview(parent, columns=columns, show="headings", height=min(10, len(rows)))
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor='center')
            for row in rows:
                tree.insert("", "end", values=[row.get(col, "") for col in columns])
            tree.pack(fill='x', padx=10, pady=5)
            self.trees.append(tree)

    def exit(self):
        for tree in getattr(self, "trees", []):
            tree.pack_forget()
        for widget in getattr(self, "parent", tk.Frame()).winfo_children():
            widget.pack_forget()

tab_spreadsheet = TabSpreadsheet()

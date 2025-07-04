from tkinter import ttk, filedialog
import tkinter as tk
from dotenv import load_dotenv
import os
import supabase as sb
import pandas as pd

load_dotenv()

class TabPDF():
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.db = sb.create_client(self.url, self.key)
        self.tables = [("ALG-450", "alg_450"), ("HX-1023", "hx_1023")]

    def enter(self, parent):
        self.parent = parent
        self.label_instructions = ttk.Label(parent, text="Select document type and enter patient name to generate PDF.", font=("Arial", 14))
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

        self.label_patient = ttk.Label(parent, text="Patient name:", font=("Arial", 12))
        self.label_patient.pack(padx=10, pady=(10, 2), anchor='w')
        self.frame_patient = ttk.Frame(parent)
        self.frame_patient.pack(fill='x', padx=10, pady=2)
        self.entry_patient = ttk.Entry(self.frame_patient, width=30)
        self.entry_patient.pack(side='left')

        self.button_generate = ttk.Button(parent, text="Generate PDF", command=self.on_generate_pdf)
        self.button_generate.pack(padx=10, pady=15)

        self.label_status = ttk.Label(parent, text="", font=("Arial", 11))
        self.label_status.pack(padx=10, pady=5)

    def on_generate_pdf(self):
        patient_name = self.entry_patient.get().strip()
        if not patient_name:
            self.label_status.config(text="Please enter a patient name.", foreground="red")
            self.entry_patient.focus_set()
            return

        doc_type_idx = self.combo_doc_type.current()
        table_name = self.tables[doc_type_idx][1]

        data = self.db.table(table_name).select("*").eq("patient", patient_name).execute()
        rows = getattr(data, "data", [])
        if not rows:
            self.label_status.config(text="No data found for this patient.", foreground="red")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF as"
        )
        if not file_path:
            self.label_status.config(text="PDF generation cancelled.", foreground="orange")
            return

        try:
            self.generate_pdf_with_pandas(file_path, rows[0], table_name)
            self.label_status.config(text=f"PDF saved to {file_path}", foreground="green")
        except Exception as e:
            self.label_status.config(text=f"Error: {e}", foreground="red")

    def generate_pdf_with_pandas(self, file_path, data, table_name):
        import matplotlib.pyplot as plt

        df = pd.DataFrame([data])
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='left')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        plt.title(f"{table_name.upper()} - Patient Report", fontsize=14, pad=20)
        plt.savefig(file_path, bbox_inches='tight')
        plt.close(fig)

    def exit(self):
        for widget in getattr(self, "parent", tk.Frame()).winfo_children():
            widget.pack_forget()

tab_pdf = TabPDF()

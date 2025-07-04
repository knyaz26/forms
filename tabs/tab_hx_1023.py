from tkinter import ttk
from dotenv import load_dotenv
import os
import tkinter as tk
import supabase as sb

load_dotenv()

class TabHX1023():
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.db = sb.create_client(self.url, self.key)

    def enter(self, parent):
        self.parent = parent
        self.lable_title = ttk.Label(parent, text="HX-1023 Tab", font=("Arial", 24))
        self.lable_title.pack(padx=10, pady=10)

        self.frame_info = ttk.Frame(parent)
        self.frame_info.pack(fill='x', padx=3, pady=5)

        self.label_patient = ttk.Label(self.frame_info, text="Patient", font=("Arial", 14))
        self.label_patient.grid(row=0, column=0, padx=3, pady=3, sticky='e')
        self.entry_patient = ttk.Entry(self.frame_info)
        self.entry_patient.grid(row=0, column=1, padx=3, pady=3, sticky='ew')

        self.label_doctor = ttk.Label(self.frame_info, text="Doctor", font=("Arial", 14))
        self.label_doctor.grid(row=0, column=2, padx=3, pady=3, sticky='e')
        self.entry_doctor = ttk.Entry(self.frame_info)
        self.entry_doctor.grid(row=0, column=3, padx=3, pady=3, sticky='ew')

        self.label_date = ttk.Label(self.frame_info, text="Date", font=("Arial", 14))
        self.label_date.grid(row=0, column=4, padx=3, pady=3, sticky='e')
        self.entry_date = ttk.Entry(self.frame_info)
        self.entry_date.grid(row=0, column=5, padx=3, pady=3, sticky='ew')

        for i in range(0, 6, 2):
            self.frame_info.columnconfigure(i, weight=0)
            self.frame_info.columnconfigure(i+1, weight=1)
        
        self.frame_observations = ttk.Frame(parent)
        self.frame_observations.pack(fill='x', padx=3, pady=5)
        self.label_observations = ttk.Label(self.frame_observations, text="Observations", font=("Arial", 14))
        self.label_observations.pack(anchor='w', padx=3, pady=3)
        self.text_observations = tk.Text(self.frame_observations, height=8, bg="#555555",fg="#eaeaea", relief='flat')
        self.text_observations.pack(fill='x', padx=3, pady=3)

        self.frame_treatments = ttk.Frame(parent)
        self.frame_treatments.pack(fill='x', padx=3, pady=5)
        self.label_treatments = ttk.Label(self.frame_treatments, text="Treatments", font=("Arial", 14))
        self.label_treatments.pack(anchor='w', padx=3, pady=3)
        self.text_treatments = tk.Text(self.frame_treatments, height=8, bg="#555555", fg="#eaeaea", relief='flat')
        self.text_treatments.pack(fill='x', padx=3, pady=3)

        self.frame_notes = ttk.Frame(parent)
        self.frame_notes.pack(fill='x', padx=3, pady=5)

        self.frame_response = ttk.Frame(self.frame_notes)
        self.frame_response.pack(side='left', fill='both', expand=True, padx=3, pady=3)
        self.label_response = ttk.Label(self.frame_response, text="Response", font=("Arial", 14))
        self.label_response.pack(anchor='w', padx=3, pady=3)
        self.text_response = tk.Text(self.frame_response, height=8, bg="#555555", fg="#eaeaea", relief='flat')
        self.text_response.pack(fill='both', expand=True, padx=3, pady=3)

        self.frame_recommendations = ttk.Frame(self.frame_notes)
        self.frame_recommendations.pack(side='right', fill='both', expand=True, padx=3, pady=3)
        self.label_recommendations = ttk.Label(self.frame_recommendations, text="Recommendations", font=("Arial", 14))
        self.label_recommendations.pack(anchor='w', padx=3, pady=3)
        self.text_recommendations = tk.Text(self.frame_recommendations, height=8, bg="#555555", fg="#eaeaea", relief='flat')
        self.text_recommendations.pack(fill='both', expand=True, padx=3, pady=3)

        self.frame_validation = ttk.Frame(parent)
        self.frame_validation.pack(fill='x', padx=3, pady=5)
        self.check_validation = ttk.Checkbutton(
            self.frame_validation,
            text="I double checked and made sure all information is correct",
            command=self.on_validation_checked
        )
        self.check_validation.pack(side='left', padx=3, pady=3)

        self.button_submit = ttk.Button(parent, text="Submit", command=self.on_button_submit_clicked, state='disabled')
        self.button_submit.pack(padx=3, pady=5)

    def on_validation_checked(self):
        if self.check_validation.instate(['selected']):
            self.button_submit.config(state='normal')
        else:
            self.button_submit.config(state='disabled')

    def on_button_submit_clicked(self):
        patient_name = self.entry_patient.get().strip()
        if not patient_name:
            self.entry_patient.focus_set()
            return
        self.submitted_data = {
            "patient": patient_name,
            "doctor": self.entry_doctor.get(),
            "date": self.entry_date.get(),
            "observations": self.text_observations.get("1.0", "end-1c"),
            "treatments": self.text_treatments.get("1.0", "end-1c"),
            "response": self.text_response.get("1.0", "end-1c"),
            "recommendations": self.text_recommendations.get("1.0", "end-1c"),
        }

        result = self.db.table("hx_1023").insert(self.submitted_data).execute()
        error = getattr(result, "error", None)
        bg = self.parent.cget("background") if "background" in self.parent.keys() else "#303030"
        if not error and hasattr(result, "status_code") and result.status_code in (200, 201):
            popup = tk.Toplevel(self.parent)
            popup.title("Success")
            popup.geometry("280x120")
            popup.configure(bg=bg)
            ttk.Label(popup, text="Data submitted successfully!", font=("Arial", 14), background=bg).pack(padx=10, pady=10)
            ttk.Button(popup, text="OK", command=popup.destroy).pack(padx=10, pady=10)
            popup.transient(self.parent)
            popup.grab_set()
            popup.focus_set()
            popup.wait_window()
        else:
            popup = tk.Toplevel(self.parent)
            popup.title("Error")
            popup.geometry("320x140")
            popup.configure(bg=bg)
            msg = "Failed to submit data. Please try again."
            if error:
                msg += f"\n{error}"
            ttk.Label(popup, text=msg, font=("Arial", 14), background=bg).pack(padx=10, pady=10)
            ttk.Button(popup, text="OK", command=popup.destroy).pack(padx=10, pady=10)
            popup.transient(self.parent)
            popup.grab_set()
            popup.focus_set()
            popup.wait_window()

        self.button_submit.config(state='disabled')
        self.entry_patient.delete(0, 'end')
        self.entry_doctor.delete(0, 'end')
        self.entry_date.delete(0, 'end')
        self.text_observations.delete("1.0", "end")
        self.text_treatments.delete("1.0", "end")
        self.text_response.delete("1.0", "end")
        self.text_recommendations.delete("1.0", "end")
        self.check_validation.state(['!selected'])

    def exit(self):
        self.lable_title.pack_forget()
        self.frame_info.pack_forget()
        self.frame_observations.pack_forget()
        self.frame_treatments.pack_forget()
        self.frame_notes.pack_forget()
        self.frame_validation.pack_forget()
        self.button_submit.pack_forget()

tab_hx_1023 = TabHX1023()
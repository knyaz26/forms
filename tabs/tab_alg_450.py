from tkinter import ttk
from dotenv import load_dotenv
import os
import tkinter as tk
import supabase as sb

load_dotenv()

class TabALG450():
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.db = sb.create_client(self.url, self.key)
        self.allergies = [
            "Peanuts", "Tree nuts", "Milk", "Eggs", "Wheat", "Soy", "Fish", "Shellfish",
            "Sesame", "Corn", "Gluten", "Mustard", "Celery", "Lupin", "Sulfites",
            "Penicillin", "Amoxicillin", "Cephalosporins", "Sulfa drugs", "Aspirin",
            "NSAIDs", "Insulin", "Anticonvulsants", "Iodine", "Contrast dye",
            "Latex", "Nickel", "Gold", "Cobalt", "Chromium", "Fragrances", "Preservatives",
            "Insect stings (bee, wasp, hornet)", "Mosquito bites", "Ant bites",
            "Pollen (grass, tree, weed)", "Dust mites", "Mold", "Animal dander (cat, dog, rodent, horse)",
            "Cockroach", "Feathers", "Sunlight (photosensitivity)", "Cold (cold urticaria)",
            "Chlorine", "Perfume", "Cosmetics", "Hair dye", "Cleaning products",
            "Red meat (alpha-gal)", "Gelatin", "Vaccine components", "Egg protein (in vaccines)",
            "Antibiotics (general)", "Antifungals", "Antivirals", "Antihistamines",
            "Shellfish iodine", "Radiocontrast media", "Tetracycline", "Macrolides",
            "Quinolones", "Carbamazepine", "Phenytoin", "Lamotrigine", "Barbiturates",
            "Opioids", "Codeine", "Morphine", "Local anesthetics", "General anesthetics",
            "Chlorhexidine", "Adhesives", "Plastics", "Rubber", "Acrylic", "Formaldehyde",
            "Parabens", "Lanolin", "Propylene glycol", "Benzalkonium chloride"
        ]
        self.allergy_vars = []

    def enter(self, parent):
        self.parent = parent
        self.lable_title = ttk.Label(parent, text="ALG-450 Tab", font=("Arial", 24))
        self.lable_title.pack(padx=10, pady=10)

        self.frame_info = ttk.Frame(parent)
        self.frame_info.pack(fill='x', padx=3, pady=5)

        self.label_patient = ttk.Label(self.frame_info, text="Patient", font=("Arial", 14))
        self.label_patient.grid(row=0, column=0, padx=3, pady=3, sticky='e')
        self.entry_patient = ttk.Entry(self.frame_info)
        self.entry_patient.grid(row=0, column=1, padx=3, pady=3, sticky='ew')

        self.label_date = ttk.Label(self.frame_info, text="Date", font=("Arial", 14))
        self.label_date.grid(row=0, column=2, padx=3, pady=3, sticky='e')
        self.entry_date = ttk.Entry(self.frame_info)
        self.entry_date.grid(row=0, column=3, padx=3, pady=3, sticky='ew')

        for i in range(0, 4, 2):
            self.frame_info.columnconfigure(i, weight=0)
            self.frame_info.columnconfigure(i+1, weight=1)

        self.frame_allergies = ttk.Frame(parent)
        self.frame_allergies.pack(fill='x', padx=3, pady=5)
        self.label_allergies = ttk.Label(self.frame_allergies, text="Allergies", font=("Arial", 14))
        self.label_allergies.pack(anchor='w', padx=3, pady=3)

        self.allergy_vars = []
        self.checkbuttons = []
        self.frame_allergy_checks = ttk.Frame(self.frame_allergies)
        self.frame_allergy_checks.pack(fill='x', padx=3, pady=3)

        rows = 12
        cols = (len(self.allergies) + rows - 1) // rows
        for idx, allergy in enumerate(self.allergies):
            row = idx % rows
            col = idx // rows
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.frame_allergy_checks, text=allergy, variable=var)
            chk.grid(row=row, column=col, sticky='w', padx=3, pady=1)
            self.allergy_vars.append(var)
            self.checkbuttons.append(chk)

        self.frame_additional = ttk.Frame(parent)
        self.frame_additional.pack(fill='x', padx=3, pady=5)
        self.label_additional = ttk.Label(self.frame_additional, text="Additional Information", font=("Arial", 14))
        self.label_additional.pack(anchor='w', padx=3, pady=3)
        self.text_additional = tk.Text(self.frame_additional, height=8, bg="#555555", fg="#eaeaea", relief='flat')
        self.text_additional.pack(fill='x', padx=3, pady=3)

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
        selected_allergies = [allergy for allergy, var in zip(self.allergies, self.allergy_vars) if var.get()]
        self.submitted_data = {
            "patient": patient_name,
            "date": self.entry_date.get(),
            "allergies": selected_allergies,
            "additional_info": self.text_additional.get("1.0", "end-1c"),
        }
        result = self.db.table("alg_450").insert(self.submitted_data).execute()
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
        self.entry_date.delete(0, 'end')
        self.text_additional.delete("1.0", "end")
        for var in self.allergy_vars:
            var.set(False)
        self.check_validation.state(['!selected'])

    def exit(self):
        self.lable_title.pack_forget()
        self.frame_info.pack_forget()
        self.frame_allergies.pack_forget()
        self.frame_additional.pack_forget()
        self.frame_validation.pack_forget()
        self.button_submit.pack_forget()

tab_alg_450 = TabALG450()


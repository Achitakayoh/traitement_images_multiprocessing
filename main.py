import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import shutil
import os
from utils import clean_and_copy_files
from traitement import apply_treatment, TREATMENTS

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

def launch_processing():
    selected_tool = combo.get()
    if not selected_tool:
        messagebox.showwarning("Traitement manquant", "Veuillez sélectionner un traitement.")
        return

    files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if not files:
        return

    # Nettoyer input/ et copier les fichiers avec noms nettoyés
    cleaned_files = clean_and_copy_files(files, INPUT_DIR)

    # Appliquer le traitement sélectionné
    tool_key = TREATMENTS[selected_tool]['key']
    treatment_fn = TREATMENTS[selected_tool]['function']

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for file in cleaned_files:
        apply_treatment(file, tool_key, treatment_fn, INPUT_DIR, OUTPUT_DIR)

    messagebox.showinfo("Succès", f"{len(cleaned_files)} image(s) traitée(s) avec succès.")

# UI
root = tk.Tk()
root.title("Traitement d'images")
root.geometry("400x150")

label = tk.Label(root, text="Choisissez un traitement :")
label.pack(pady=10)

combo = ttk.Combobox(root, values=list(TREATMENTS.keys()), state="readonly")
combo.pack(pady=5)

button = tk.Button(root, text="Sélectionner les fichiers et traiter", command=launch_processing)
button.pack(pady=20)

root.mainloop()

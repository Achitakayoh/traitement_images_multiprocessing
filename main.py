import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import shutil
import os
import subprocess
import platform
from utils import clean_and_copy_files
from traitement import apply_treatment, TREATMENTS

INPUT_DIR = 'input'

ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
SENSITIVE_PATHS = ['C:\\Windows', '/etc', '/bin', '/usr']  # dossiers à éviter

def is_valid_file(path):
    ext = os.path.splitext(path)[1].lower()
    abs_path = os.path.abspath(path)
    return (
        ext in ALLOWED_EXTENSIONS and
        not any(abs_path.startswith(s) for s in SENSITIVE_PATHS)
    )

def open_folder(path):
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir le dossier : {e}")

def launch_processing():
    selected_tool = combo.get()
    if not selected_tool:
        messagebox.showwarning("Traitement manquant", "Veuillez sélectionner un traitement.")
        return

    selected_files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if not selected_files:
        return

    # Filtrer les fichiers valides
    files = [f for f in selected_files if is_valid_file(f)]
    if not files:
        messagebox.showerror("Erreur", "Aucun fichier valide ou autorisé n’a été sélectionné.")
        return

    output_dir = filedialog.askdirectory(title="Choisissez le dossier de destination")
    if not output_dir:
        messagebox.showwarning("Annulé", "Aucun dossier sélectionné pour l'enregistrement.")
        return

    output_dir = os.path.abspath(output_dir)

    try:
        cleaned_files = clean_and_copy_files(files, INPUT_DIR)
        tool_key = TREATMENTS[selected_tool]['key']
        treatment_fn = TREATMENTS[selected_tool]['function']

        for file in cleaned_files:
            apply_treatment(file, tool_key, treatment_fn, INPUT_DIR, output_dir)

        if messagebox.askyesno("Terminé", f"{len(cleaned_files)} image(s) traitée(s) avec succès.\n\nOuvrir le dossier ?"):
            open_folder(output_dir)

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# UI
root = tk.Tk()
root.title("Traitement d'images")
root.geometry("400x150")
root.resizable(False, False)

label = tk.Label(root, text="Choisissez un traitement :")
label.pack(pady=10)

combo = ttk.Combobox(root, values=list(TREATMENTS.keys()), state="readonly")
combo.pack(pady=5)

button = tk.Button(root, text="Sélectionner les fichiers et traiter", command=launch_processing)
button.pack(pady=20)

root.mainloop()

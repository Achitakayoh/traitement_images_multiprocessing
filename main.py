import os
import subprocess
import platform
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from utils import clean_and_copy_files
from traitement import apply_treatment, TREATMENTS

INPUT_DIR = 'input'
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
SENSITIVE_PATHS = ['C:\\Windows', '/etc', '/bin', '/usr']

last_input_dir = os.path.expanduser('~/Downloads')
last_output_dir = os.path.expanduser('~/')
selected_files = []
selected_output_dir = ""

def is_valid_file(path):
    ext = os.path.splitext(path)[1].lower()
    abs_path = os.path.abspath(path)
    return ext in ALLOWED_EXTENSIONS and not any(abs_path.startswith(s) for s in SENSITIVE_PATHS)

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

def select_input_files():
    global selected_files, last_input_dir
    files = filedialog.askopenfilenames(
        title="Sélectionner les images à traiter",
        initialdir=last_input_dir,
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if files:
        last_input_dir = os.path.dirname(files[0])
        selected_files[:] = [f for f in files if is_valid_file(f)]
        short_list = ", ".join([os.path.basename(f) for f in selected_files[:3]])
        if len(selected_files) > 3:
            short_list += ", ..."
        input_label.config(text=f"{len(selected_files)} fichier(s) : {short_list}")

def select_output_directory():
    global selected_output_dir, last_output_dir
    folder = filedialog.askdirectory(title="Choisir le dossier de destination", initialdir=last_output_dir)
    if folder:
        last_output_dir = folder
        selected_output_dir = folder
        output_label.config(text=f"Dossier : {selected_output_dir}")

def launch_processing():
    if not selected_files:
        messagebox.showwarning("Images manquantes", "Veuillez d'abord sélectionner des images.")
        return
    if not selected_output_dir:
        messagebox.showwarning("Destination manquante", "Veuillez d'abord sélectionner un dossier de destination.")
        return

    selected_tool = combo.get()
    if not selected_tool:
        messagebox.showwarning("Traitement manquant", "Veuillez sélectionner un traitement.")
        return

    try:
        cleaned_files = clean_and_copy_files(selected_files, INPUT_DIR)
        tool_key = TREATMENTS[selected_tool]['key']
        treatment_fn = TREATMENTS[selected_tool]['function']

        for file in cleaned_files:
            apply_treatment(file, tool_key, treatment_fn, INPUT_DIR, selected_output_dir)

        if messagebox.askyesno("Terminé", f"{len(cleaned_files)} image(s) traitée(s) avec succès.\n\nOuvrir le dossier ?"):
            open_folder(selected_output_dir)

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# Interface avec ttkbootstrap
root = ttk.Window(themename="flatly")
root.title("🖼️ Traitement d'images")
root.geometry("500x340")
root.resizable(False, False)

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=BOTH, expand=True)

ttk.Label(main_frame, text="Étape 1 - Sélection des images", font=("Segoe UI", 10, "bold")).pack(anchor=W, pady=(0, 5))
ttk.Button(main_frame, text="📁 Parcourir…", command=select_input_files, bootstyle="primary").pack(anchor=W)
input_label = ttk.Label(main_frame, text="Aucun fichier sélectionné")
input_label.pack(anchor=W, pady=(0, 15))

ttk.Label(main_frame, text="Étape 2 - Dossier de destination", font=("Segoe UI", 10, "bold")).pack(anchor=W, pady=(0, 5))
ttk.Button(main_frame, text="📂 Choisir le dossier", command=select_output_directory, bootstyle="info").pack(anchor=W)
output_label = ttk.Label(main_frame, text="Aucun dossier sélectionné")
output_label.pack(anchor=W, pady=(0, 15))

ttk.Label(main_frame, text="Étape 3 - Type de traitement", font=("Segoe UI", 10, "bold")).pack(anchor=W, pady=(0, 5))
combo = ttk.Combobox(main_frame, values=list(TREATMENTS.keys()), state="readonly", width=35)
combo.pack(anchor=W, pady=(0, 20))

ttk.Button(main_frame, text="▶ Lancer le traitement", command=launch_processing, bootstyle="success").pack(anchor=CENTER)

root.mainloop()
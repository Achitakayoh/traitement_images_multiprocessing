import os
from tkinter import filedialog, messagebox
from typing import Any

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, CENTER, W

from core import config
from core.traitement import TREATMENTS, apply_treatment
from core.utils import clean_and_copy_files, is_valid_file


class ImageApp:
    def __init__(self, root: Any) -> None:
        self.root = root
        self.root.title("🖼️ Traitement d'images")
        self.root.geometry("500x340")
        self.root.resizable(False, False)

        self.selected_files: list[str] = []
        self.selected_output_dir: str = ""
        self.last_input_dir: str = config.DEFAULT_INPUT
        self.last_output_dir: str = config.DEFAULT_OUTPUT

        self.build_ui()

    def build_ui(self) -> None:
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # Étape 1
        ttk.Label(
            main_frame,
            text="Étape 1 - Sélection des images",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor=W)
        ttk.Button(
            main_frame,
            text="📁 Parcourir…",
            command=self.select_input_files,
            bootstyle="primary",  # type: ignore[arg-type]
        ).pack(anchor=W, pady=2)
        self.input_label = ttk.Label(main_frame, text="Aucun fichier sélectionné")
        self.input_label.pack(anchor=W, pady=(0, 15))

        # Étape 2
        ttk.Label(
            main_frame,
            text="Étape 2 - Dossier de destination",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor=W)
        ttk.Button(
            main_frame,
            text="📂 Choisir le dossier",
            command=self.select_output_directory,
            bootstyle="info",  # type: ignore[arg-type]
        ).pack(anchor=W, pady=2)
        self.output_label = ttk.Label(main_frame, text="Aucun dossier sélectionné")
        self.output_label.pack(anchor=W, pady=(0, 15))

        # Étape 3
        ttk.Label(
            main_frame,
            text="Étape 3 - Type de traitement",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor=W)
        self.combo = ttk.Combobox(
            main_frame,
            values=list(TREATMENTS.keys()),
            state="readonly",
            width=35,
        )
        self.combo.pack(anchor=W, pady=(0, 20))

        ttk.Button(
            main_frame,
            text="▶ Lancer le traitement",
            command=self.launch_processing,
            bootstyle="success",  # type: ignore[arg-type]
        ).pack(anchor=CENTER)

    def select_input_files(self) -> None:
        files = filedialog.askopenfilenames(
            title="Sélectionner les images à traiter",
            initialdir=self.last_input_dir,
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif")],
        )
        if files:
            self.last_input_dir = os.path.dirname(files[0])
            self.selected_files = [f for f in files if is_valid_file(f)]
            short_list = ", ".join(
                [os.path.basename(f) for f in self.selected_files[:3]]
            )
            if len(self.selected_files) > 3:
                short_list += ", ..."
            self.input_label.config(
                text=f"{len(self.selected_files)} fichier(s) : {short_list}"
            )

    def select_output_directory(self) -> None:
        folder = filedialog.askdirectory(
            title="Choisir le dossier de destination",
            initialdir=self.last_output_dir,
        )
        if folder:
            self.last_output_dir = folder
            self.selected_output_dir = folder
            self.output_label.config(text=f"Dossier : {self.selected_output_dir}")

    def launch_processing(self) -> None:
        if not self.selected_files:
            messagebox.showwarning(
                "Images manquantes", "Veuillez d'abord sélectionner des images."
            )  # type: ignore
            return
        if not self.selected_output_dir:
            messagebox.showwarning(
                "Destination manquante",
                "Veuillez d'abord sélectionner un dossier de destination.",
            )  # type: ignore
            return
        if not self.combo.get():
            messagebox.showwarning(
                "Traitement manquant", "Veuillez sélectionner un traitement."
            )  # type: ignore
            return

        try:
            cleaned_files = clean_and_copy_files(self.selected_files, config.INPUT_DIR)
            tool_key = TREATMENTS[self.combo.get()]["key"]
            treatment_fn = TREATMENTS[self.combo.get()]["function"]

            for file in cleaned_files:
                apply_treatment(
                    file,
                    tool_key,
                    treatment_fn,
                    config.INPUT_DIR,
                    self.selected_output_dir,
                )

            if messagebox.askyesno(
                "Terminé",
                f"{len(cleaned_files)} image(s) traitée(s) avec succès.\n\n"
                "Ouvrir le dossier ?",
            ):  # type: ignore
                self.open_folder(self.selected_output_dir)

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")  # type: ignore

    def open_folder(self, path: str) -> None:
        try:
            if os.name == "nt":
                os.startfile(path)  # noqa: S606
            elif os.name == "posix":
                # S603/S607: usage contrôlé, chemin local, pas d'entrée utilisateur
                import subprocess

                subprocess.run(
                    ["xdg-open", os.path.abspath(path)], check=False
                )  # noqa: S603, S607
            elif os.name == "mac":
                import subprocess

                subprocess.run(
                    ["open", os.path.abspath(path)], check=False
                )  # noqa: S603, S607
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le dossier : {e}")  # type: ignore

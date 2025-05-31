# Point d'entrée avec UI (Tkinter)
import multiprocessing
from PIL import Image
import os

# Dossiers d'entrée et de sortie
INPUT_DIR = "input"
OUTPUT_DIR = "output"


def process_image(image_name):
    """Convertit une image en niveaux de gris et la sauvegarde dans le dossier output."""
    input_path = os.path.join(INPUT_DIR, image_name)
    output_path = os.path.join(OUTPUT_DIR, f"processed_{image_name}")

    try:
        with Image.open(input_path) as img:
            grayscale = img.convert("L")  # Conversion en niveaux de gris
            grayscale.save(output_path)
            print(f"[OK] {image_name} traitée → {output_path}")
    except Exception as e:
        print(f"[ERREUR] Impossible de traiter {image_name} : {e}")


if __name__ == "__main__":
    # Crée le dossier de sortie s'il n'existe pas
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Liste des fichiers images dans le dossier input
    image_files = [
        f
        for f in os.listdir(INPUT_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
    ]

    if not image_files:
        print("Aucune image trouvée dans le dossier 'input'.")
    else:
        # Lancement du traitement en parallèle
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            pool.map(process_image, image_files)

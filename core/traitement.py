# Fonctions de traitement (grayscale, rotation, etc.)
from PIL import Image, ImageOps, ImageFilter
import os

# Dictionnaire des traitements
TREATMENTS = {
    "Niveau de gris"       : {"key": "black",  "function": lambda img: img.convert("L")},
    "Rotation 90°"         : {"key": "rotate", "function": lambda img: img.rotate(90, expand=True)},
    "Redimensionner 50%"   : {"key": "resize", "function": lambda img: img.resize((img.width // 2, img.height // 2))},
    "Inverser les couleurs": {"key": "invert", "function": lambda img: ImageOps.invert(img.convert("RGB"))},
    "Flouter légèrement"   : {"key": "blur",   "function": lambda img: img.filter(ImageFilter.GaussianBlur(2))},
}

def apply_treatment(image_name, tool_key, treatment_fn, input_dir, output_dir):
    in_path = os.path.join(input_dir, image_name)
    out_path = os.path.join(output_dir, f"processed_{tool_key}_{image_name}")

    try:
        with Image.open(in_path) as img:
            processed = treatment_fn(img)
            processed.save(out_path)
            print(f"[OK] {image_name} → {out_path}")
    except Exception as e:
        print(f"[ERREUR] {image_name} : {e}")

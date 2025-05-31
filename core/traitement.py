import os
from collections.abc import Callable
from typing import Any

from PIL import Image, ImageFilter, ImageOps


def grayscale(img: Image.Image) -> Image.Image:
    return img.convert("L")


def rotate(img: Image.Image) -> Image.Image:
    return img.rotate(90, expand=True)


def resize(img: Image.Image) -> Image.Image:
    return img.resize((img.width // 2, img.height // 2))


def invert(img: Image.Image) -> Image.Image:
    return ImageOps.invert(img.convert("RGB"))


def blur(img: Image.Image) -> Image.Image:
    return img.filter(ImageFilter.GaussianBlur(2))


TREATMENTS: dict[str, dict[str, Any]] = {
    "Niveau de gris": {
        "key": "black",
        "function": grayscale,
    },
    "Rotation 90°": {
        "key": "rotate",
        "function": rotate,
    },
    "Redimensionner 50%": {
        "key": "resize",
        "function": resize,
    },
    "Inverser les couleurs": {
        "key": "invert",
        "function": invert,
    },
    "Flouter légèrement": {
        "key": "blur",
        "function": blur,
    },
}


def apply_treatment(
    image_name: str,
    tool_key: str,
    treatment_fn: Callable[[Image.Image], Image.Image],
    input_dir: str,
    output_dir: str,
) -> None:
    in_path = os.path.join(input_dir, image_name)
    out_path = os.path.join(output_dir, f"processed_{tool_key}_{image_name}")
    try:
        with Image.open(in_path) as img:
            processed = treatment_fn(img)
            processed.save(out_path)
            print(f"[OK] {image_name} → {out_path}")
    except Exception as e:
        print(f"[ERREUR] {image_name} : {e}")

import os
import shutil
import unicodedata
import re
from core import config

def clean_filename(filename):
    name, ext = os.path.splitext(filename)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    return name + ext

def clean_and_copy_files(filepaths, target_dir):
    shutil.rmtree(target_dir, ignore_errors=True)
    os.makedirs(target_dir, exist_ok=True)

    used_names = set()
    cleaned_files = []

    for path in filepaths:
        base_name = os.path.basename(path)
        clean_name = clean_filename(base_name)
        base, ext = os.path.splitext(clean_name)

        # Gestion des doublons
        i = 1
        final_name = clean_name
        while final_name in used_names:
            final_name = f"{base}_{i}{ext}"
            i += 1

        used_names.add(final_name)
        dest_path = os.path.join(target_dir, final_name)
        shutil.copy(path, dest_path)
        cleaned_files.append(final_name)

    return cleaned_files

def is_valid_file(path):
    ext = os.path.splitext(path)[1].lower()
    abs_path = os.path.abspath(path)
    return (
        ext in config.ALLOWED_EXTENSIONS and
        not any(abs_path.startswith(s) for s in config.SENSITIVE_PATHS)
    )

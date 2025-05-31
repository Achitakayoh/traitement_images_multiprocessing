import os
import tempfile
import shutil
import pytest
from core import utils


class DummyConfig:
    ALLOWED_EXTENSIONS = {".jpg", ".png"}
    SENSITIVE_PATHS = [os.path.abspath(os.sep)]


def test_clean_filename():
    assert utils.clean_filename("imâge testé.png") == "image_teste.png"
    assert utils.clean_filename("fichier@#éè!.jpg") == "fichier__ee_.jpg"
    assert utils.clean_filename("normal-file.JPG") == "normal-file.JPG"


def test_clean_and_copy_files(monkeypatch):
    # Patch config to avoid using real SENSITIVE_PATHS
    monkeypatch.setattr(utils, "config", DummyConfig)
    with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as dst_dir:
        # Create files with special chars and duplicates
        filenames = ["imâge testé.png", "imâge testé.png", "fichier@#éè!.jpg"]
        src_files = []
        for name in filenames:
            path = os.path.join(src_dir, name)
            with open(path, "w") as f:
                f.write("data")
            src_files.append(path)
        result = utils.clean_and_copy_files(src_files, dst_dir)
        # Should clean names and handle duplicates
        assert result[0] == "image_teste.png"
        assert result[1] == "image_teste_1.png"
        assert result[2] == "fichier__ee_.jpg"
        # Files exist in dst_dir
        for name in result:
            assert os.path.exists(os.path.join(dst_dir, name))


def test_is_valid_file(monkeypatch):
    monkeypatch.setattr(utils, "config", DummyConfig)
    # Valid extension, not sensitive path
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as f:
        assert utils.is_valid_file(f.name)
    # Invalid extension
    with tempfile.NamedTemporaryFile(suffix=".exe", delete=True) as f:
        assert not utils.is_valid_file(f.name)
    # Sensitive path
    sensitive = os.path.join(os.sep, "test.jpg")
    assert not utils.is_valid_file(sensitive)

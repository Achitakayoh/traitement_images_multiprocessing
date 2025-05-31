import os
import tempfile

import pytest

from core import utils


class DummyConfig:
    ALLOWED_EXTENSIONS = {".jpg", ".png"}
    SENSITIVE_PATHS = [os.path.abspath(os.sep)]


def test_clean_filename() -> None:
    assert utils.clean_filename("imâge testé.png") == "image_teste.png"  # noqa: S101
    assert utils.clean_filename("fichier@#éè!.jpg") == "fichier__ee_.jpg"  # noqa: S101
    assert utils.clean_filename("normal-file.JPG") == "normal-file.JPG"  # noqa: S101


def test_clean_and_copy_files(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(utils, "config", DummyConfig)
    with (
        tempfile.TemporaryDirectory() as src_dir,
        tempfile.TemporaryDirectory() as dst_dir,
    ):
        filenames = ["imâge testé.png", "imâge testé.png", "fichier@#éè!.jpg"]
        src_files: list[str] = []
        for name in filenames:
            path = os.path.join(src_dir, name)
            with open(path, "w") as f:
                f.write("data")
            src_files.append(path)
        result = utils.clean_and_copy_files(src_files, dst_dir)
        assert result[0] == "image_teste.png"  # noqa: S101
        assert result[1] == "image_teste_1.png"  # noqa: S101
        assert result[2] == "fichier__ee_.jpg"  # noqa: S101
        for name in result:
            assert os.path.exists(os.path.join(dst_dir, name))  # noqa: S101


def test_is_valid_file(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(utils, "config", DummyConfig)
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) as f:
        assert utils.is_valid_file(f.name)  # noqa: S101
    with tempfile.NamedTemporaryFile(suffix=".exe", delete=True) as f:
        assert not utils.is_valid_file(f.name)  # noqa: S101
    sensitive = os.path.join(os.sep, "test.jpg")
    assert not utils.is_valid_file(sensitive)  # noqa: S101

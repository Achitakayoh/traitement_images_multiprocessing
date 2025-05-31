import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def test_files_dir() -> str:
    dir_path = os.path.join(os.path.dirname(__file__), "test_files")
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


@pytest.fixture(scope="function")
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path

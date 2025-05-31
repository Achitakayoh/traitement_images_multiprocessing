import pytest
from playwright.sync_api import Browser, Page
import os


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
    }


@pytest.fixture(scope="session")
def test_files_dir():
    dir_path = os.path.join(os.path.dirname(__file__), "test_files")
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


@pytest.fixture(scope="function")
def temp_dir(tmp_path):
    return tmp_path

import os

INPUT_DIR: str = "input"
ALLOWED_EXTENSIONS: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
SENSITIVE_PATHS: list[str] = ["C:\\Windows", "/etc", "/bin", "/usr"]
DEFAULT_INPUT: str = os.path.expanduser("~/Downloads")
DEFAULT_OUTPUT: str = os.path.expanduser("~/")

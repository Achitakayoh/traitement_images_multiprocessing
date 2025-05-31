import os

INPUT_DIR = 'input'
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
SENSITIVE_PATHS = ['C:\\Windows', '/etc', '/bin', '/usr']

DEFAULT_INPUT = os.path.expanduser('~/Downloads')
DEFAULT_OUTPUT = os.path.expanduser('~/')

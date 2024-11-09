import os

def get_version():
    return os.getenv('VERSION', '0.0.1')

__version__ = get_version()

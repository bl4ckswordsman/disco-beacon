import platform
from PySide6.QtCore import QOperatingSystemVersion


def is_linux():
    return platform.system() == 'Linux'

def is_windows_11():
    """Check if the current system is Windows 11."""
    return QOperatingSystemVersion.current() >= QOperatingSystemVersion.Windows11

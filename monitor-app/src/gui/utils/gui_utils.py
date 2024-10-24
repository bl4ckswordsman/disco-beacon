import platform
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette
from src.gui.utils.gui_config import gui_config

def get_current_theme():
    app = QApplication.instance()
    if app:
        palette = app.palette()
        return 'dark' if palette.color(QPalette.ColorRole.Window).lightness() < 128 else 'light'
    return 'light'  # Default to light theme if app instance is not available

def get_icon_path(theme: str) -> str:
    if platform.system() == 'Linux':
        return f"{gui_config.ICON_THEME_DARK}/{gui_config.ICON_NAME}"
    icon_theme = gui_config.ICON_THEME_LIGHT if theme == 'light' else gui_config.ICON_THEME_DARK
    return f"{icon_theme}/{gui_config.ICON_NAME}"

def is_linux():
    return platform.system() == 'Linux'

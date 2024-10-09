from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette
from ..gui.gui_config import gui_config

def get_current_theme():
    app = QApplication.instance()
    if app:
        palette = app.palette()
        return 'dark' if palette.color(QPalette.Window).lightness() < 128 else 'light'
    return 'light'  # Default to light theme if app instance is not available

def get_icon_path(theme: str) -> str:
    icon_theme = gui_config.ICON_THEME_LIGHT if theme == 'light' else gui_config.ICON_THEME_DARK
    return f"{icon_theme}/{gui_config.ICON_NAME}"

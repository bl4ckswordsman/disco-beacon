from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette
from src.gui.utils.gui_config import gui_config
from src.gui.utils.platform_utils import is_linux


def get_current_theme():
    app = QApplication.instance()
    if app:
        palette = app.palette()
        return 'dark' if palette.color(QPalette.ColorRole.Window).lightness() < 128 else 'light'
    return 'light'  # Default to light theme if app instance is not available

def get_icon_path(theme: str) -> str:
    if is_linux():
        return f"{gui_config.ICON_THEME_DARK}/{gui_config.ICON_NAME}"
    icon_theme = gui_config.ICON_THEME_LIGHT if theme == 'light' else gui_config.ICON_THEME_DARK
    return f"{icon_theme}/{gui_config.ICON_NAME}"

def apply_mica_transparency(window):
    window.setAttribute(Qt.WA_TranslucentBackground)
    window.setWindowFlag(Qt.FramelessWindowHint)
    window.setStyleSheet("background: rgba(255, 255, 255, 0.8);")

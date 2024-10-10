from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication

def get_system_theme():
    app = QApplication.instance()
    if app is None:
        return "light"
    palette = app.palette()
    if palette.color(QPalette.Window).lightness() > 128:
        return "light"
    else:
        return "dark"

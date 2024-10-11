try:
    from PySide6.QtWidgets import QSystemTrayIcon, QMenu
    from PySide6.QtGui import QIcon
    from PySide6.QtCore import Signal
except ImportError:
    from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
    from PyQt6.QtGui import QIcon
    from PyQt6.QtCore import pyqtSignal as Signal

from src.gui.utils.gui_config import gui_config
from src.gui.utils.app_settings import AppSettings

class SystemTrayIcon(QSystemTrayIcon):
    exit_app = Signal()

    def __init__(self, parent=None):
        icon = QIcon(gui_config.ICON_THEME_DARK + '/' + gui_config.ICON_NAME)  # Always use dark theme
        super().__init__(icon, parent)
        self.setToolTip(AppSettings.APP_NAME)
        self.create_context_menu()

    def create_context_menu(self):
        menu = QMenu()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.emit_exit_signal)
        self.setContextMenu(menu)

    def emit_exit_signal(self):
        self.exit_app.emit()

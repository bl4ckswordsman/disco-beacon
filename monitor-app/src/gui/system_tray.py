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

    def __init__(self, parent=None, theme='light'):
        from src.gui.utils.gui_utils import get_icon_path
        icon = QIcon(get_icon_path(theme))
        super().__init__(icon, parent)
        self.setToolTip(AppSettings.APP_NAME)
        self.create_context_menu()

    def update_icon(self, theme):
        from src.gui.utils.gui_utils import get_icon_path
        self.setIcon(QIcon(get_icon_path(theme)))

    def create_context_menu(self):
        menu = QMenu()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_app.emit)
        self.setContextMenu(menu)

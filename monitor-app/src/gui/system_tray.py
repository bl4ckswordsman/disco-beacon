try:
    from PySide6.QtWidgets import QSystemTrayIcon, QMenu
    from PySide6.QtGui import QIcon
    from PySide6.QtCore import Signal
except ImportError:
    from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
    from PyQt6.QtGui import QIcon
    from PyQt6.QtCore import pyqtSignal as Signal

from src.gui.utils.app_settings import AppSettings
from src.gui.utils.gui_utils import get_icon_path
from src.gui.utils.platform_utils import is_linux


class SystemTrayIcon(QSystemTrayIcon):
    exit_app = Signal()

    def __init__(self, parent=None, theme='light'):
        icon = QIcon(get_icon_path('dark' if is_linux() else theme))
        super().__init__(icon, parent)
        self.setToolTip(AppSettings.APP_NAME)
        self.create_context_menu()

    def update_icon(self, theme):
        if not is_linux():
            self.setIcon(QIcon(get_icon_path(theme)))

    def create_context_menu(self):
        menu = QMenu()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_app.emit)
        self.setContextMenu(menu)

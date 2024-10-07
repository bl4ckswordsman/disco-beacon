from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal

class SystemTrayIcon(QSystemTrayIcon):
    exit_app = Signal()

    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.setToolTip('Game Server Monitor')
        self.create_context_menu()

    def create_context_menu(self):
        menu = QMenu()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.emit_exit_signal)
        self.setContextMenu(menu)

    def emit_exit_signal(self):
        self.exit_app.emit()

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QSystemTrayIcon, QApplication
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from ..core.config import Config
from ..core.logger import logger
from .system_tray import SystemTrayIcon

class MainWindow(QMainWindow):
    exit_app = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Server Monitor")
        self.setGeometry(100, 100, Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

        # Set window icon
        self.setWindowIcon(QIcon(Config.ICON_PATH))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.tray_icon = None

        logger.info("MainWindow initialized")

    def handle_exit(self):
        logger.info("Exit signal received from system tray")
        self.close()
        self.exit_app.emit()

    def update_status(self, status):
        logger.debug(f"Updating status: {status}")
        self.status_label.setText(status)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Game Server Monitor",
            "Application minimized to tray",
            QSystemTrayIcon.Information,
            2000
        )

    def show_window(self):
        self.show()
        self.activateWindow()

    def set_tray_icon(self, tray_icon):
        self.tray_icon = tray_icon
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.activateWindow()

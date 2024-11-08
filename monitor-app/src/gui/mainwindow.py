try:
    from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QSystemTrayIcon, QPushButton
    from PySide6.QtCore import Qt, Signal, QTimer
    from PySide6.QtGui import QIcon, QFont
    from PySide6.QtCore import QOperatingSystemVersion
except ImportError:
    from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QSystemTrayIcon, QPushButton
    from PyQt6.QtCore import Qt, pyqtSignal as Signal, QTimer
    from PyQt6.QtGui import QIcon, QFont

from src.gui.settings_dialog import SettingsDialog
from src.gui.utils.gui_config import gui_config
from ..core.logger import logger
from src.gui.utils.gui_utils import get_current_theme, is_linux
from src.gui.utils.app_settings import AppSettings
from src.core.constants import CHECK_INTERVAL


from src.gui.utils.platform_utils import is_windows_11
class MainWindow(QMainWindow):
    is_minimized = False
    exit_app = Signal()
    theme_changed = Signal(str)

    def __init__(self):
        super().__init__()
        if is_windows_11():
            # Make window background transparent for Mica effect
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            # Ensure window frame is enabled for Mica
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, False)
        self.setWindowTitle(AppSettings.APP_NAME)
        self.setGeometry(100, 100, gui_config.WINDOW_WIDTH, gui_config.WINDOW_HEIGHT)
        self.current_theme = get_current_theme()
        self.set_window_icon()

        self.theme_timer = QTimer(self)
        self.theme_timer.timeout.connect(self.check_and_update_theme)
        self.theme_timer.start(1000)  # Check every second

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setFont(QFont(gui_config.FONT_FAMILY, gui_config.FONT_SIZE_LARGE))
        layout.addWidget(self.status_label)

        settings_button = QPushButton("Settings")
        settings_button.setFont(QFont(gui_config.FONT_FAMILY, gui_config.FONT_SIZE_LARGE))
        settings_button.clicked.connect(self.open_settings_dialog)
        layout.addWidget(settings_button)

        self.tray_icon = None

        self.theme_changed.connect(self.update_theme)

        self.status_timeout_timer = QTimer(self)
        self.status_timeout_timer.timeout.connect(self.handle_status_timeout)
        self.status_timeout_timer.setSingleShot(True)

        logger.info("MainWindow initialized")

        # Initialize the app with a status message
        self.update_status("Initializing...")

    def open_settings_dialog(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            logger.info("Settings updated")

    def set_window_icon(self):
        icon = QIcon(gui_config.WINDOW_ICON_PNG)
        self.setWindowIcon(icon)
        logger.info(f"Window icon set to: {gui_config.WINDOW_ICON_PNG}")

    def update_theme(self, new_theme):
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            if self.tray_icon and not is_linux():
                self.tray_icon.update_icon(new_theme)
            logger.info(f"Theme updated to: {new_theme}")
            self.theme_changed.emit(new_theme)

    def check_and_update_theme(self):
        new_theme = get_current_theme()
        if new_theme != self.current_theme:
            self.update_theme(new_theme)

    def handle_exit(self):
        logger.info("Exit signal received from system tray")
        self.close()
        self.exit_app.emit()

    def update_status(self, status):
        logger.debug(f"Updating status: {status}")
        if not self.is_minimized:
            # Stop any existing timer before starting a new one
            self.status_timeout_timer.stop()
            self.status_label.setText(status)
            # Start a new timeout timer with double the check interval
            self.status_timeout_timer.start(CHECK_INTERVAL * 1000 * 2)

    def handle_status_timeout(self):
        logger.warning("Status update timeout")
        self.status_label.setText("Error: No updates")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.is_minimized = True
        if self.tray_icon:
            self.tray_icon.showMessage(
                AppSettings.APP_NAME,
                "Application minimized to tray",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )

    def show_window(self):
        self.show()
        self.activateWindow()
        self.is_minimized = False

    def set_tray_icon(self, tray_icon):
        self.tray_icon = tray_icon
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
                self.is_minimized = True
            else:
                self.show()
                self.activateWindow()
                self.is_minimized = False

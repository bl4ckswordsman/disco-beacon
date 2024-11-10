from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QPushButton, QComboBox, QLabel
from PySide6.QtCore import Signal, Qt
from src.version import __version__
from src.core.app_settings import settings_loader
from src.core import constants
from src.gui.utils.platform_utils import is_windows_11
from src.gui.utils.mica_utils import apply_mica_to_window

class SettingsDialog(QDialog):
    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        if is_windows_11():
            apply_mica_to_window(self)
        self.layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.webhook_url = QLineEdit(settings_loader.get_setting('webhook_url'))
        form_layout.addRow("Webhook URL:", self.webhook_url)

        self.api_key = QLineEdit(settings_loader.get_setting('api_key'))
        form_layout.addRow("Steam API Key:", self.api_key)

        self.steam_id = QLineEdit(settings_loader.get_setting('steam_id'))
        form_layout.addRow("Steam ID:", self.steam_id)

        self.check_interval = QSpinBox()
        self.check_interval.setValue(settings_loader.get_setting('check_interval'))
        self.check_interval.setRange(1, 3600)
        form_layout.addRow("Check Interval (seconds):", self.check_interval)

        self.game_selector = QComboBox()
        self.game_selector.addItems(constants.SUPPORTED_GAMES.values())
        self.game_selector.setCurrentText(constants.SUPPORTED_GAMES.get(settings_loader.get_setting('game_app_id'), "Valheim"))
        form_layout.addRow("Game:", self.game_selector)

        self.monitor_mode = QComboBox()
        self.monitor_mode.addItems(['Both', 'Server Only'])
        self.monitor_mode.setCurrentText(settings_loader.get_setting('monitor_mode', 'Both'))
        form_layout.addRow("Monitor Mode:", self.monitor_mode)

        self.layout.addLayout(form_layout)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(save_button)

        # Add build version at bottom with styling
        self.build_version_label = QLabel(f"Version {__version__}")
        self.build_version_label.setStyleSheet("""
            QLabel {
                font-size: 9pt;
                padding: 5px;
            }
        """)
        self.build_version_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.build_version_label)

    def save_settings(self):
        app_settings.set('webhook_url', self.webhook_url.text())
        app_settings.set('api_key', self.api_key.text())
        app_settings.set('steam_id', self.steam_id.text())
        app_settings.set('check_interval', self.check_interval.value())
        app_settings.set('game_app_id', [k for k, v in constants.SUPPORTED_GAMES.items() if v == self.game_selector.currentText()][0])
        app_settings.set('monitor_mode', self.monitor_mode.currentText().lower())
        self.accept()

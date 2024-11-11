from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QPushButton, QComboBox, QLabel, QCheckBox, QFrame)
from PySide6.QtCore import Signal
from src.version import __version__
from src.core.app_settings import settings_loader, settings_saver, handle_autorun_change
from src.core import constants
from src.gui.utils.platform_utils import is_windows_11, is_windows
from src.gui.utils.mica_utils import apply_mica_to_window
from src.core.version_checker import fetch_latest_version, compare_versions
import webbrowser

class SettingsDialog(QDialog):
    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        if is_windows_11():
            apply_mica_to_window(self)
        self.layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        # Create form fields
        self.webhook_url = QLineEdit(settings_loader.get_setting('webhook_url'))
        self.webhook_url.setEchoMode(QLineEdit.EchoMode.Password)
        self.webhook_url.setPlaceholderText("Enter Discord webhook URL")
        form_layout.addRow("Webhook URL:", self.webhook_url)

        self.api_key = QLineEdit(settings_loader.get_setting('api_key'))
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key.setPlaceholderText("Enter Steam API key")
        form_layout.addRow("Steam API Key:", self.api_key)

        self.steam_id = QLineEdit(settings_loader.get_setting('steam_id'))
        self.steam_id.setPlaceholderText("Enter Steam ID")
        form_layout.addRow("Steam ID:", self.steam_id)

        self.check_interval = QSpinBox()
        self.check_interval.setValue(settings_loader.get_setting('check_interval'))
        self.check_interval.setRange(1, 3600)
        form_layout.addRow("Check Interval (seconds):", self.check_interval)

        self.game_selector = QComboBox()
        self.game_selector.addItems(constants.SUPPORTED_GAMES.values())
        current_game = constants.SUPPORTED_GAMES[settings_loader.get_setting('game_app_id')]
        self.game_selector.setCurrentText(current_game)
        form_layout.addRow("Game:", self.game_selector)

        self.monitor_mode = QComboBox()
        self.monitor_mode.addItems(['Both', 'Server Only'])
        self.monitor_mode.setCurrentText(settings_loader.get_setting('monitor_mode', 'Both').title())
        form_layout.addRow("Monitor Mode:", self.monitor_mode)

        self.auto_run_checkbox = QCheckBox("Run on system startup")
        if is_windows():
            self.auto_run_checkbox.setChecked(settings_loader.get_setting('auto_run', False))
        else:
            self.auto_run_checkbox.setEnabled(False)
            self.auto_run_checkbox.setToolTip("Auto-run is only supported on Windows")
        form_layout.addRow(self.auto_run_checkbox)

        self.layout.addLayout(form_layout)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(save_button)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(separator)

        # Create horizontal layout for version info
        version_layout = QHBoxLayout()

        # Version label
        self.version_label = QLabel("Checking for updates...")
        self.version_label.setStyleSheet("font-size: 9pt;")
        version_layout.addWidget(self.version_label)

        # Update button (smaller than regular buttons)
        self.update_button = QPushButton("View Update")
        self.update_button.setStyleSheet("""
            QPushButton {
                font-size: 9pt;
                padding: 2px 8px;
                max-height: 20px;
            }
        """)
        self.update_button.clicked.connect(self.open_latest_release_page)
        self.update_button.hide()  # Hidden by default until update is available
        version_layout.addWidget(self.update_button)

        version_layout.addStretch()  # Push everything to the left
        self.layout.addLayout(version_layout)

        self.fetch_and_compare_versions()

    def fetch_and_compare_versions(self):
        latest_version = fetch_latest_version()
        if latest_version:
            comparison_result = compare_versions(__version__, latest_version)
            self.version_label.setText(comparison_result)
            # Show update button only if newer version is available
            if "→" in comparison_result:
                self.update_button.show()
        else:
            self.version_label.setText("Version check failed")

    def open_latest_release_page(self):
        webbrowser.open("https://github.com/bl4ckswordsman/disco-beacon/releases/latest")

    def save_settings(self):
        # Save all non-autorun settings first
        settings_saver.set_setting('webhook_url', self.webhook_url.text())
        settings_saver.set_setting('api_key', self.api_key.text())
        settings_saver.set_setting('steam_id', self.steam_id.text())
        settings_saver.set_setting('check_interval', self.check_interval.value())
        settings_saver.set_setting('game_app_id', [k for k, v in constants.SUPPORTED_GAMES.items() if v == self.game_selector.currentText()][0])
        settings_saver.set_setting('monitor_mode', self.monitor_mode.currentText().lower())

        # Handle autorun setting separately to apply changes immediately
        autorun_enabled = self.auto_run_checkbox.isChecked()

        # Handle autorun changes
        autorun_enabled = self.auto_run_checkbox.isChecked()
        registry_updated = handle_autorun_change(autorun_enabled)
        settings_saved = settings_saver.set_setting('auto_run', registry_updated and autorun_enabled)

        if is_windows() and not registry_updated:
            self.auto_run_checkbox.setChecked(False)
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Settings Error",
                "Failed to save autorun settings. Make sure you have the necessary permissions."
            )
            return

        if not settings_saved:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self,
                "Settings Error",
                "Failed to save settings. Make sure you have write permissions in your config directory."
            )
            return

        self.accept()

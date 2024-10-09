from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
import sys
from .gui_config import gui_config
from .mainwindow import MainWindow
from .system_tray import SystemTrayIcon
from ..core.steam_api import get_status
from ..core.logger import logger
import resources.resources # noqa: F401

def init_gui():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Set Fusion style for better theme support
    window = MainWindow()
    tray_icon = SystemTrayIcon(window)
    tray_icon.show()

    # Connect tray icon's exit signal to a function that will quit the application
    tray_icon.exit_app.connect(lambda: (app.quit(), sys.exit(0)))

    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda: update_gui(window))
    timer.start(gui_config.GUI_REFRESH_RATE)

    logger.info("GUI initialized with system tray icon and Fusion style")
    return app, window, tray_icon

def update_gui(window):
    try:
        game_status, server_status, lobby_id, server_owner, _ = get_status()
        status_text = f"Game: {game_status}, Server: {server_status}"
        if server_status == 'online':
            status_text += f"\nLobby ID: {lobby_id}\nServer Owner: {server_owner}"
        window.update_status(status_text)
        logger.debug(f"GUI updated: {status_text}")
    except Exception as e:
        logger.error(f"Error updating GUI: {e}")

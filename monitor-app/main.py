import sys
import time
from src.core.config import config
from src.core.steam_api import get_status
from src.core.logger import logger
from src.core.notification_handler import setup_notification_handlers
from src.core.state import GameState, GameServerState

# GUI imports
gui_available = False
try:
    from PySide6 import QtWidgets, QtCore, QtGui
    from src.gui.mainwindow import MainWindow
    from src.gui.system_tray import SystemTrayIcon
    gui_available = True
except ImportError as e:
    logger.warning(f"PySide6 import error: {e}")
    logger.warning("GUI functionality will be disabled.")
except Exception as e:
    logger.error(f"Unexpected error importing PySide6: {e}")
    logger.warning("GUI functionality will be disabled.")

def update_gui(window):
    try:
        game_status, server_status, lobby_id, server_owner, _ = get_status()
        status_text = f"Game: {game_status}, Server: {server_status}"
        if server_status == 'online':
            status_text += f"\nLobby ID: {lobby_id}\nServer Owner: {server_owner}"
        window.update_status(status_text)
        logger.info(f"GUI updated: {status_text}")
    except Exception as e:
        logger.error(f"Error updating GUI: {e}")

def init_gui():
    if not gui_available:
        return None, None, None

    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        icon = QtGui.QIcon(config.ICON_PATH)
        tray_icon = SystemTrayIcon(icon, window)
        tray_icon.show()

        # Connect tray icon's exit signal to a function that will quit the application
        tray_icon.exit_app.connect(lambda: (app.quit(), sys.exit(0)))

        window.set_tray_icon(tray_icon)
        window.show()

        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: update_gui(window))
        timer.start(config.GUI_REFRESH_RATE)

        logger.info("GUI initialized with system tray icon")
        return app, window, tray_icon
    except Exception as e:
        logger.error(f"Failed to set up GUI components: {e}")
        return None, None, None

def main() -> None:
    """Main function to continuously check game and server status."""
    logger.info("Application starting")
    setup_notification_handlers()
    game_state = GameState()
    game_server_state = GameServerState()

    app, window, tray_icon = init_gui() if gui_available else (None, None, None)

    if app and window and tray_icon:
        logger.info("Running in GUI mode with system tray icon")
    elif gui_available:
        logger.warning("Failed to initialize GUI completely. Falling back to CLI mode.")
    else:
        logger.info("Running in CLI mode")

    try:
        while True:
            try:
                game_status, server_status, lobby_id, server_owner, server_data = get_status()

                if config.MONITOR_MODE == 'both':
                    logger.info(f"Game status: {game_status}, Server status: {server_status}")
                    game_state.update(status=game_status)
                else:
                    logger.info(f"Server status: {server_status}")

                game_server_state.update(
                    status=server_status,
                    lobby_id=lobby_id,
                    server_owner=server_owner or "Unknown",
                    server_data=server_data
                )

                if window:
                    update_gui(window)

            except Exception as e:
                logger.error(f"Error occurred while fetching status: {e}")

            if app:
                app.processEvents()
            else:
                time.sleep(config.CHECK_INTERVAL)

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    finally:
        if app:
            app.quit()

    logger.info("Application shutting down")

if __name__ == "__main__":
    main()

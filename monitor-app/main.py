import time
from src.core.config import config
from src.core.steam_api import get_status
from src.core.logger import logger
from src.core.notification_handler import setup_notification_handlers
from src.core.state import GameState, GameServerState
from src.gui.gui_init import init_gui

from src.gui.app_settings import AppSettings

gui_available = False

try:
    import PySide6
    from PySide6 import QtWidgets, QtCore, QtGui
    from src.gui.mainwindow import MainWindow
    from src.gui.system_tray import SystemTrayIcon
    gui_available = all((PySide6, QtWidgets, QtCore, QtGui, MainWindow, SystemTrayIcon))
except ImportError as e:
    logger.warning(f"PySide6 import error: {e}")
    logger.warning("GUI functionality will be disabled.")
except Exception as e:
    logger.error(f"Unexpected error importing PySide6: {e}")
    logger.warning("GUI functionality will be disabled.")

if not gui_available:
    logger.warning("GUI functionality is disabled.")

def check_and_update_status(game_state, game_server_state, window):
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

        if window and not window.is_minimized:
            window.update_status(f"Game: {game_status}, Server: {server_status}")

    except Exception as e:
        logger.error(f"Error occurred while fetching status: {e}")

def setup_application():
    if gui_available:
        AppSettings.set_app_metadata()
    logger.info("Application setup completed")

def main() -> None:
    """Main function to continuously check game and server status."""
    logger.info("Application starting")

    setup_application()

    setup_notification_handlers()
    game_state = GameState()
    game_server_state = GameServerState()

    last_check = time.time()
    app, window, tray_icon = init_gui() if gui_available else (None, None, None)

    if app and window and tray_icon:
        logger.info("Running in GUI mode")
        try:
            while True:
                current_time = time.time()
                if current_time - last_check >= config.CHECK_INTERVAL:
                    check_and_update_status(game_state, game_server_state, window)
                    last_check = current_time
                app.processEvents()
                time.sleep(0.1)  # Short sleep to prevent busy-waiting
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
        finally:
            app.quit()
    else:
        logger.info("Running in CLI mode")
        try:
            while True:
                current_time = time.time()
                if current_time - last_check >= config.CHECK_INTERVAL:
                    check_and_update_status(game_state, game_server_state, None)
                    last_check = current_time
                time.sleep(0.1)  # Short sleep to prevent busy-waiting
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")

    logger.info("Application shutting down")

if __name__ == "__main__":
    main()

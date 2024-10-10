import time
from src.core.config import config
from src.core.steam_api import get_status
from src.core.logger import logger
from src.core.notification_handler import setup_notification_handlers
from src.core.state import GameState, GameServerState
from src.gui.utils.gui_init import init_gui
from src.gui.utils.app_settings import AppSettings
from src.core.app_settings import app_settings
gui_available = False

try:
    from PySide6 import QtWidgets, QtCore, QtGui
    from src.gui.mainwindow import MainWindow
    from src.gui.system_tray import SystemTrayIcon
    gui_available = all((QtWidgets, QtCore, QtGui, MainWindow, SystemTrayIcon))
except ImportError as e:
    logger.warning(f"GUI import error: {e}")
    logger.warning("GUI functionality will be disabled.")
except Exception as e:
    logger.error(f"Unexpected error importing GUI modules: {e}")
    logger.warning("GUI functionality will be disabled.")

if not gui_available:
    logger.warning("GUI functionality is disabled.")

def check_and_update_status(game_state, game_server_state, window):
    try:
        api_key = app_settings.get('api_key', '')
        steam_id = app_settings.get('steam_id', '')
        game_app_id = int(app_settings.get('game_app_id', '0'))
        game_status, server_status, lobby_id, server_owner, server_data = get_status(api_key, steam_id, game_app_id)

        game_name = config.get_game_name(game_app_id)
        monitor_mode = app_settings.get('monitor_mode', 'both')

        logger.info(f"Game status: {game_status}, Server status: {server_status}")

        # Always update game state regardless of monitor mode
        game_state.update(status=game_status)

        # Update server state
        game_server_state.update(
            status=server_status,
            lobby_id=lobby_id,
            server_owner=server_owner or "Unknown",
            server_data=server_data
        )

        if window and not window.is_minimized:
            status_text = f"{game_name} - Game: {game_status}, Server: {server_status}"
            window.update_status(status_text)

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

    if gui_available:
        logger.info("Running in GUI mode")
    else:
        logger.info("Running in CLI mode")

    try:
        while True:
            current_time = time.time()
            if current_time - last_check >= app_settings.get('check_interval'):
                check_and_update_status(game_state, game_server_state, window)
                last_check = current_time
            if gui_available:
                app.processEvents()
            time.sleep(0.1)  # Short sleep to prevent busy-waiting
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    finally:
        if gui_available:
            app.quit()

    logger.info("Application shutting down")

if __name__ == "__main__":
    main()

import time
from src.core.config import config
from src.core.steam_api import fetch_status_from_api
from src.core.logger import logger
from src.core.notification_handler import setup_notification_handlers
from src.core.state import GameState, GameServerState
from src.gui.utils.gui_init import init_gui
from src.gui.utils.app_settings import AppSettings
from src.core.app_settings import settings_loader, settings_saver, handle_autorun_change
from src.gui.utils.platform_utils import is_windows
from src.core.version_checker import fetch_latest_version, compare_versions
from src.core.single_instance import SingleInstance

gui_available = False

def import_gui_modules():
    global gui_available
    try:
        import PySide6
        from PySide6 import QtWidgets, QtCore, QtGui
        from src.gui.mainwindow import MainWindow
        from src.gui.system_tray import SystemTrayIcon
        gui_available = all((PySide6, QtWidgets, QtCore, QtGui, MainWindow, SystemTrayIcon))
    except ImportError as e:
        logger.warning(f"GUI import error: {e}")
        logger.warning("GUI functionality will be disabled.")
    except Exception as e:
        logger.error(f"Unexpected error importing GUI modules: {e}")
        logger.warning("GUI functionality will be disabled.")

    if not gui_available:
        logger.warning("GUI functionality is disabled.")


import_gui_modules()

def fetch_status():
    try:
        api_key = settings_loader.get_setting('api_key', '')
        steam_id = settings_loader.get_setting('steam_id', '')
        game_app_id = int(settings_loader.get_setting('game_app_id', '0'))
        game_status, server_status, lobby_id, server_owner, server_data = fetch_status_from_api(api_key, steam_id, game_app_id)
        return game_status, server_status, lobby_id, server_owner, server_data
    except Exception as e:
        logger.error(f"Error occurred while fetching status: {e}")
        return None, None, None, None, None

def update_status(game_state, game_server_state, window, game_status, server_status, lobby_id, server_owner, server_data):
    game_name = config.get_game_name(settings_loader.get_setting('game_app_id'))

    logger.info(f"Game status: {game_status}, Server status: {server_status}")

    game_state.update_state(status=game_status)

    game_server_state.update_state(
        status=server_status,
        lobby_id=lobby_id,
        server_owner=server_owner or "Unknown",
        server_data=server_data
    )

    if window and not window.is_minimized:
        if game_status is None or server_status is None:
            status_text = "Error: Could not fetch status\nCheck your settings and connection"
        else:
            status_text = (f"{game_name} \nGame: {'Online ✅' if game_status == 'online' else 'Offline ❌'}"
                         f"\nServer: {'Online ✅' if server_status == 'online' else 'Offline ❌'}")
        window.refresh_status(status_text)
    elif window is None:
        if game_status is None or server_status is None:
            print("Error: Could not fetch status")
        else:
            print(f"{game_name} - Game: {game_status}, Server: {server_status}")

def initialize_application():
    if gui_available:
        AppSettings.set_app_metadata()
    logger.info("Application setup completed")

    if is_windows():
        # Handle autorun based on saved setting
        auto_run_enabled = settings_loader.get_setting('auto_run', False)
        if not handle_autorun_change(auto_run_enabled):
            settings_saver.set_setting('auto_run', False)

def check_for_updates(tray_icon=None):
    latest_version = fetch_latest_version()
    if latest_version:
        comparison_result = compare_versions(AppSettings.VERSION, latest_version)
        if "→" in comparison_result:
            logger.info(comparison_result)
            if gui_available and tray_icon:
                from PySide6.QtWidgets import QSystemTrayIcon
                tray_icon.showMessage(
                    "Update Available",
                    comparison_result,
                    QSystemTrayIcon.MessageIcon.Information,
                    5000  # Show for 5 seconds
                )

def main() -> None:
    logger.info("Application starting")

    with SingleInstance("/tmp/disco_beacon.lock") as instance:
        if not instance:
            logger.error("Another instance of the application is already running.")
            return

        initialize_application()

        setup_notification_handlers()
        game_state = GameState()
        game_server_state = GameServerState()

        last_check = time.time()

        if gui_available:
            logger.info("Running in GUI mode")
            app, window, tray_icon = init_gui()
            check_for_updates(tray_icon)
            try:
                while True:
                    current_time = time.time()
                    if current_time - last_check >= settings_loader.get_setting('check_interval'):
                        game_status, server_status, lobby_id, server_owner, server_data = fetch_status()
                        update_status(game_state, game_server_state, window, game_status, server_status, lobby_id, server_owner, server_data)
                        last_check = current_time
                    app.processEvents()
                    time.sleep(0.1)
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt, shutting down...")
            finally:
                app.quit()
        else:
            logger.info("Running in CLI mode")
            try:
                while True:
                    current_time = time.time()
                    if current_time - last_check >= settings_loader.get_setting('check_interval'):
                        game_status, server_status, lobby_id, server_owner, server_data = fetch_status()
                        update_status(game_state, game_server_state, None, game_status, server_status, lobby_id, server_owner, server_data)
                        last_check = current_time
                    time.sleep(0.1)
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt, shutting down...")

        logger.info("Application shutting down")


if __name__ == "__main__":
    main()

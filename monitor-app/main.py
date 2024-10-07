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
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer
    from src.gui.mainwindow import MainWindow
    gui_available = True
except ImportError:
    logger.warning("PySide6 is not installed. GUI functionality will be disabled.")

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
        return None, None

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    timer = QTimer()
    timer.timeout.connect(lambda: update_gui(window))
    timer.start(config.GUI_REFRESH_RATE)

    logger.info("GUI initialized")
    return app, window

def main() -> None:
    """Main function to continuously check game and server status."""
    logger.info("Application starting")
    setup_notification_handlers()
    game_state = GameState()
    game_server_state = GameServerState()

    if gui_available:
        app, window = init_gui()
        if app:
            logger.info("Starting GUI event loop")
            sys.exit(app.exec())
    else:
        logger.info("Running in CLI mode")
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

            except Exception as e:
                logger.error(f"Error occurred: {e}")
                logger.error(f"Failed to fetch status. Retrying in {config.CHECK_INTERVAL} seconds.")

            time.sleep(config.CHECK_INTERVAL)

if __name__ == "__main__":
    main()

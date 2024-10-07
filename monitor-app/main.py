import time
from config import config
from steam_api import get_server_status
from logger import logger
from notification_handler import setup_notification_handlers
from state import GameState, GameServerState

def main() -> None:
    """Main function to continuously check server status."""
    setup_notification_handlers()
    game_state = GameState()
    game_server_state = GameServerState()

    while True:
        try:
            status, lobby_id, server_owner, server_data = get_server_status()
            logger.info(f"Game server status: {status}")

            game_state.update(
                status='online' if status == 'online' else 'offline'
            )

            game_server_state.update(
                status=status,
                lobby_id=lobby_id,
                server_owner=server_owner or "Unknown",
                server_data=server_data
            )

        except Exception as e:
            logger.error(f"Error occurred: {e}")
            logger.error(f"Failed to fetch server status. Retrying in {config.CHECK_INTERVAL} seconds.")

        time.sleep(config.CHECK_INTERVAL)


if __name__ == "__main__":
    main()

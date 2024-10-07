import time
from config import config
from steam_api import get_status
from logger import logger
from notification_handler import setup_notification_handlers
from state import GameState, GameServerState

def main() -> None:
    """Main function to continuously check game and server status."""
    setup_notification_handlers()
    game_state = GameState()
    game_server_state = GameServerState()

    while True:
        try:
            # Check game and server status
            game_status, server_status, lobby_id, server_owner, server_data = get_status()
            logger.info(f"Game status: {game_status}, Server status: {server_status}")

            game_state.update(
                status=game_status
            )

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

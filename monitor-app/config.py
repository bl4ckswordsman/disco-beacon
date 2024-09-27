from typing import Dict, Optional
import constants
import keys
from steam_api import get_game_icon

class Config:
    API_KEY: str = keys.API_KEY
    SERVER_OWNER_STEAM_ID: str = keys.SERVER_OWNER_STEAM_ID
    GAME_APP_ID: int = constants.GAME_APP_ID
    CHECK_INTERVAL: int = constants.CHECK_INTERVAL
    WEBHOOK_URL: str = keys.WEBHOOK_URL
    SUPPORTED_GAMES: Dict[int, str] = constants.SUPPORTED_GAMES

    @classmethod
    def get_game_name(cls, app_id: int) -> str:
        return cls.SUPPORTED_GAMES.get(app_id, "Unknown Game")

    @classmethod
    def get_game_icon_url(cls, app_id: int) -> Optional[str]:
        return get_game_icon(app_id)

config = Config()
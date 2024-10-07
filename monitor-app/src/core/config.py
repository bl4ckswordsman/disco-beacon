from typing import Dict, Optional
from . import constants
from . import keys
from .steam_api import get_game_icon

class Config:
    # GUI Configuration
    WINDOW_WIDTH: int = 800
    WINDOW_HEIGHT: int = 600
    GUI_REFRESH_RATE: int = 1000
    COLORS: Dict[str, str] = {
        'background': '#F0F0F0',
        'text': '#333333',
        'accent': '#007BFF',
        'online': '#28A745',
        'offline': '#DC3545'
    }
    FONT_FAMILY: str = 'Arial'
    FONT_SIZE_NORMAL: int = 12
    FONT_SIZE_LARGE: int = 16
    ICON_PATH: str = 'assets/icons/'

    API_KEY: str = keys.API_KEY
    SERVER_OWNER_STEAM_ID: str = keys.SERVER_OWNER_STEAM_ID

    GAME_APP_ID: int = constants.GAME_APP_ID

    CHECK_INTERVAL: int = constants.CHECK_INTERVAL
    MONITOR_MODE: str = 'both'  # 'both' or 'server_only'

    WEBHOOK_URL: str = keys.WEBHOOK_URL
    SUPPORTED_GAMES: Dict[int, str] = constants.SUPPORTED_GAMES

    @classmethod
    def get_game_name(cls, app_id: int) -> str:
        return cls.SUPPORTED_GAMES.get(app_id, "Unknown Game")

    @classmethod
    def get_game_icon_url(cls, app_id: int) -> Optional[str]:
        return get_game_icon(app_id)


config = Config()

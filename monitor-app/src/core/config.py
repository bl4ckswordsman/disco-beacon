from . import constants, keys
from .steam_api import get_game_icon

class Config:
    APP_NAME = 'Disco Beacon'
    API_KEY = keys.API_KEY
    SERVER_OWNER_STEAM_ID = keys.SERVER_OWNER_STEAM_ID
    GAME_APP_ID = constants.GAME_APP_ID
    CHECK_INTERVAL = constants.CHECK_INTERVAL
    MONITOR_MODE = 'both'  # 'both' or 'server_only'
    WEBHOOK_URL = keys.WEBHOOK_URL
    SUPPORTED_GAMES = constants.SUPPORTED_GAMES

    @staticmethod
    def get_game_name(app_id):
        return Config.SUPPORTED_GAMES.get(app_id, "Unknown Game")

    @staticmethod
    def get_game_icon_url(app_id):
        return get_game_icon(app_id)

config = Config()

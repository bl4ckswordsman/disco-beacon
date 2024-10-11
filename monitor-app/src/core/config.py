from . import constants
from .app_settings import app_settings
from .steam_api import get_game_icon

class Config:
    APP_NAME = 'Disco Beacon'
    API_KEY = app_settings.get('api_key', '')
    SERVER_OWNER_STEAM_ID = app_settings.get('steam_id', '')
    GAME_APP_ID = app_settings.get('game_app_id', constants.GAME_APP_ID)
    CHECK_INTERVAL = app_settings.get('check_interval', constants.CHECK_INTERVAL)
    MONITOR_MODE = app_settings.get('monitor_mode', 'both')  # 'both' or 'server_only'
    WEBHOOK_URL = app_settings.get('webhook_url', '')
    SUPPORTED_GAMES = constants.SUPPORTED_GAMES

    @staticmethod
    def get_game_name(app_id):
        return Config.SUPPORTED_GAMES.get(app_id, "Unknown Game")

    @staticmethod
    def get_game_icon_url(app_id):
        return get_game_icon(app_id)


config = Config()

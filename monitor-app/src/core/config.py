from . import constants
from .app_settings import settings_loader
from .steam_api import fetch_game_icon


class Config:
    APP_NAME = 'Disco Beacon'
    API_KEY = settings_loader.get_setting('api_key', '')
    SERVER_OWNER_STEAM_ID = settings_loader.get_setting('steam_id', '')
    GAME_APP_ID = settings_loader.get_setting('game_app_id', constants.GAME_APP_ID)
    CHECK_INTERVAL = settings_loader.get_setting('check_interval', constants.CHECK_INTERVAL)
    MONITOR_MODE = settings_loader.get_setting('monitor_mode', 'both')  # 'both' or 'server_only'
    WEBHOOK_URL = settings_loader.get_setting('webhook_url', '')
    SUPPORTED_GAMES = constants.SUPPORTED_GAMES

    @staticmethod
    def get_game_name(app_id):
        return Config.SUPPORTED_GAMES.get(app_id, "Unknown Game")

    @staticmethod
    def get_game_icon_url(app_id):
        return fetch_game_icon(app_id)


config = Config()

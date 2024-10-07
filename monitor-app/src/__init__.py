from . import core
from . import gui  # GUI package initialization

# Core package initialization
from .core.config import Config
from .core.constants import *
from .core.events import EventEmitter
from .core.logger import logger
from .core.notification_handler import setup_notification_handlers
from .core.state import GameState, GameServerState
from .core.steam_api import get_status, get_game_icon
from .core.webhook import send_webhook_notification

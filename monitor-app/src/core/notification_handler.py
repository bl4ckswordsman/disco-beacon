from typing import Dict, Optional
from .config import config
from .logger import logger
from .webhook import send_webhook_notification
from datetime import datetime, timezone
from .constants import GREEN_CIRCLE, YELLOW_CIRCLE, RED_CIRCLE, SUPPORTED_GAMES
from .events import event_emitter
from .app_settings import settings_loader


def setup_notification_handlers():
    event_emitter.on('game_state_changed', handle_game_state_change)
    event_emitter.on('game_server_state_changed', handle_game_server_state_change)

def handle_game_state_change(state, old_status, new_status):
    # Ignore transitions involving None/error states
    if old_status is None or new_status is None:
        logger.info(f"Ignoring state change involving error state: {old_status} -> {new_status}")
        return

    monitor_mode = settings_loader.get_setting('monitor_mode', 'both')
    game_app_id = settings_loader.get_setting('game_app_id')
    game_name = SUPPORTED_GAMES.get(game_app_id, "Unknown Game")
    icon_url = config.get_game_icon_url(game_app_id)
    current_time = datetime.now(timezone.utc).isoformat()

    if monitor_mode == 'both':
        if new_status == 'online' and old_status == 'offline':
            notify_game_online(game_name, current_time, icon_url)
        elif new_status == 'offline' and old_status == 'online':
            notify_game_offline(game_name, current_time, icon_url)
    else:
        logger.info(f"Game state change detected: {old_status} -> {new_status}")

def handle_game_server_state_change(state, old_status, new_status):
    # Ignore transitions involving None/error states
    if old_status is None or new_status is None:
        logger.info(f"Ignoring server state change involving error state: {old_status} -> {new_status}")
        return

    game_app_id = settings_loader.get_setting('game_app_id')
    game_name = SUPPORTED_GAMES.get(game_app_id, "Unknown Game")
    icon_url = config.get_game_icon_url(game_app_id)
    current_time = datetime.now(timezone.utc).isoformat()

    if new_status == 'online' and old_status == 'offline':
        notify_server_online(game_name, state.server_owner, state.lobby_id or "Unknown", current_time, icon_url)
    elif new_status == 'offline' and old_status == 'online':
        notify_server_offline(game_name, state.server_owner, current_time, icon_url)

def notify_game_online(game_name: str, current_time: str, icon_url: Optional[str]):
    logger.info(f"{game_name} is now running")
    send_webhook_notification(settings_loader.get_setting('webhook_url'), {
        "content": f"{game_name} is now running!",
        "embeds": [{
            "title": f"{YELLOW_CIRCLE} Game Running",
            "description": f"{game_name} is running, but the server is down",
            "color": 16776960,  # Yellow color
            "timestamp": current_time,
            "footer": {"text": "Last updated"},
            "thumbnail": {"url": icon_url} if icon_url else {}
        }]
    })

def notify_game_offline(game_name: str, current_time: str, icon_url: Optional[str]):
    logger.info(f"{game_name} is now offline")
    send_webhook_notification(settings_loader.get_setting('webhook_url'), {
        "content": f"{game_name} is no longer running",
        "embeds": [{
            "title": f"{RED_CIRCLE} Game Offline",
            "description": f"No active {game_name} instance",
            "color": 15548997,  # Red color
            "timestamp": current_time,
            "footer": {"text": "Last updated"},
            "thumbnail": {"url": icon_url} if icon_url else {}
        }]
    })

def notify_server_offline(game_name: str, server_owner: str, current_time: str, icon_url: Optional[str]):
    logger.info(f"{game_name} server owned by {server_owner} is now offline")
    send_webhook_notification(settings_loader.get_setting('webhook_url'), {
        "content": f"The {game_name} server is down! @everyone",
        "embeds": [{
            "title": f"{RED_CIRCLE} Server Offline",
            "description": f"No active {game_name} server",
            "color": 15548997,  # Red color
            "fields": [
                {"name": "Steam Host", "value": server_owner, "inline": True}
            ],
            "timestamp": current_time,
            "footer": {"text": "Last updated"},
            "thumbnail": {"url": icon_url} if icon_url else {}
        }]
    })

def notify_server_online(game_name: str, server_owner: str, lobby_id: Optional[str], current_time: str, icon_url: Optional[str]):
    logger.info(f"{game_name} server owned by {server_owner} is now online with lobby ID: {lobby_id}")
    send_webhook_notification(
        settings_loader.get_setting('webhook_url'),
        {
            "content": f"The {game_name} server is up! @everyone",
            "embeds": [{
                "title": f"{GREEN_CIRCLE} Server Online",
                "description": f"Lobby ID: {lobby_id}",
                "color": 5763719,  # Green color
                "fields": [
                    {"name": "Steam Host", "value": server_owner, "inline": True}
                ],
                "timestamp": current_time,
                "footer": {"text": "Last updated"},
                "thumbnail": {"url": icon_url} if icon_url else {}
            }]
        }
    )

def log_online_details(server_data: Dict):
    logger.info(f"Game: {server_data.get('gameextrainfo', 'Unknown')}")
    logger.info(f"Server IP: {server_data.get('gameserverip', 'Unknown')}")
    logger.info(f"Server started: {server_data.get('lastlogoff', 'Unknown')}")
    if 'gameserversteamid' in server_data:
        logger.info(f"Server Steam ID: {server_data['gameserversteamid']}")

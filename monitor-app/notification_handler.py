from typing import Dict, Optional
from config import config
from logger import logger
from webhook import send_webhook_notification
from datetime import datetime, timezone
from constants import GREEN_CIRCLE, YELLOW_CIRCLE, RED_CIRCLE
from events import event_emitter
from state import server_state

def setup_notification_handlers():
    event_emitter.on('state_changed', handle_state_change)

def handle_state_change(state, old_state, new_state):
    game_name = config.get_game_name(config.GAME_APP_ID)
    icon_url = config.get_game_icon_url(config.GAME_APP_ID)
    current_time = datetime.now(timezone.utc).isoformat()

    if new_state != old_state:
        if new_state == 'offline':
            send_offline_notification(game_name, state.server_owner, current_time, icon_url)
        elif new_state == 'online_incomplete':
            send_incomplete_notification(game_name, state.server_owner, current_time, icon_url)
        elif new_state == 'online_complete':
            send_online_notification(game_name, state.server_owner, state.lobby_id or "Unknown", current_time, icon_url)

def send_offline_notification(game_name: str, server_owner: str, current_time: str, icon_url: Optional[str]):
    logger.info(f"{game_name} server owned by {server_owner} is now offline")
    send_webhook_notification(config.WEBHOOK_URL, {
        "content": f"The {game_name} server is down!",
        "embeds": [{
            "title": f"{RED_CIRCLE} Offline",
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


def send_incomplete_notification(game_name: str, server_owner: str, current_time: str, icon_url: Optional[str]):
    logger.warning(f"{game_name} server owned by {server_owner} is now online but complete data is missing")
    send_webhook_notification(config.WEBHOOK_URL, {
        "content": f"{game_name} is running, but the server is down!",
        "embeds": [{
            "title": f"{YELLOW_CIRCLE} Offline",
            "description": "Game is running but the server is down",
            "color": 16776960,  # Yellow color
            "fields": [
                {"name": "Steam Host", "value": server_owner, "inline": True}
            ],
            "timestamp": current_time,
            "footer": {"text": "Last updated"},
            "thumbnail": {"url": icon_url} if icon_url else {}
        }]
    })

def send_online_notification(game_name: str, server_owner: str, lobby_id: Optional[str], current_time: str, icon_url: Optional[str]):
    logger.info(f"{game_name} server owned by {server_owner} is now online with lobby ID: {lobby_id}")
    send_webhook_notification(
        config.WEBHOOK_URL,
        {
            "content": f"The {game_name} server is up!",
            "embeds": [{
                "title": f"{GREEN_CIRCLE} Online",
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

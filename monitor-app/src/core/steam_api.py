import requests
from typing import Dict, Optional, Tuple
from .keys import API_KEY, SERVER_OWNER_STEAM_ID
from .constants import GAME_APP_ID
from .logger import logger

def get_status() -> Tuple[str, str, Optional[str], Optional[str], Optional[Dict]]:
    """
    Fetch game and server status from Steam API.

    Returns:
        Tuple containing game status ('online' or 'offline'),
        server status ('online' or 'offline'),
        lobby ID (if server online),
        server owner name,
        and server data.
    """
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={API_KEY}&steamids={SERVER_OWNER_STEAM_ID}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        server_owner = data['response']['players'][0]

        game_status = 'offline'
        server_status = 'offline'
        lobby_id = None

        if 'gameid' in server_owner and int(server_owner['gameid']) == GAME_APP_ID:
            game_status = 'online'
            lobby_id = server_owner.get('lobbysteamid')
            if lobby_id:
                server_status = 'online'

        return game_status, server_status, lobby_id, server_owner.get('personaname'), server_owner
    except requests.RequestException:
        raise

def get_game_icon(app_id: int) -> Optional[str]:
    """
    Fetch game icon URL from Steam Store API.

    Args:
        app_id (int): The Steam AppID of the game.

    Returns:
        Optional[str]: URL of the game icon (capsule image), or None if not found.
    """
    url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if str(app_id) in data and data[str(app_id)]['success']:
            app_data = data[str(app_id)]['data']
            # Prefer capsule_image if available, otherwise use header_image
            return app_data.get('capsule_image') or app_data.get('header_image')

        logger.warning(f"No icon found for app_id {app_id}")
        return None
    except requests.RequestException as e:
        logger.error(f"Failed to fetch game icon for app_id {app_id}: {e}")
        return None

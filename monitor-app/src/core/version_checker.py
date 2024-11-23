import requests
from .logger import logger

GITHUB_API_URL = "https://api.github.com/repos/bl4ckswordsman/disco-beacon/releases/latest"

def fetch_latest_version():
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        latest_release = response.json()
        # Strip 'v' prefix if present to ensure consistent comparison
        return latest_release["tag_name"].lstrip('v')
    except requests.RequestException as e:
        logger.error(f"Error fetching latest version: {e}")
        return None

def compare_versions(current_version, latest_version):
    # Strip 'v' prefix if present
    current = current_version.lstrip('v')
    latest = latest_version.lstrip('v')

    try:
        # Convert version strings to tuples of integers for proper comparison
        current_parts = tuple(map(int, current.split('.')))
        latest_parts = tuple(map(int, latest.split('.')))
    except ValueError as e:
        logger.error(f"Error comparing versions: {e}")
        return f"Invalid version format: {current_version} or {latest_version}"

    if current_parts >= latest_parts:
        return f"v{current} (Latest ✅)"
    else:
        return f"Update available: v{current} → v{latest}"

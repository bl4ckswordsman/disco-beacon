import requests
from src.version import __version__

GITHUB_API_URL = "https://api.github.com/repos/bl4ckswordsman/disco-beacon/releases/latest"

def fetch_latest_version():
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        latest_release = response.json()
        # Strip 'v' prefix if present to ensure consistent comparison
        return latest_release["tag_name"].lstrip('v')
    except requests.RequestException as e:
        print(f"Error fetching latest version: {e}")
        return None

def compare_versions(current_version, latest_version):
    # Strip 'v' prefix if present
    current = current_version.lstrip('v')
    latest = latest_version.lstrip('v')

    # Convert version strings to tuples of integers for proper comparison
    current_parts = tuple(map(int, current.split('.')))
    latest_parts = tuple(map(int, latest.split('.')))

    if current_parts >= latest_parts:
        return "You are using the latest version."
    else:
        return f"A new version ({latest_version}) is available. Please update."

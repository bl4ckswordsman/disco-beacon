import requests
from src.version import __version__

GITHUB_API_URL = "https://api.github.com/repos/bl4ckswordsman/disco-beacon/releases/latest"

def fetch_latest_version():
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        latest_release = response.json()
        return latest_release["tag_name"]
    except requests.RequestException as e:
        print(f"Error fetching latest version: {e}")
        return None

def compare_versions(current_version, latest_version):
    if current_version == latest_version:
        return "You are using the latest version."
    else:
        return f"A new version ({latest_version}) is available. Please update."

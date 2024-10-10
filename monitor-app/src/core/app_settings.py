import json
import os

class AppSettings:
    def __init__(self):
        self.settings_file = 'settings.json'
        self.default_settings = {
            'webhook_url': '',
            'api_key': '',
            'steam_id': '',
            'check_interval': 10,
            'game_app_id': 892970,  # Valheim's App ID as default
            'monitor_mode': 'both'
        }
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return self.default_settings

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key, default=None):
        return self.settings.get(key, self.default_settings.get(key, default))

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

app_settings = AppSettings()

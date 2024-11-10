import json
import os

class SettingsLoader:
    def __init__(self, settings_file='settings.json'):
        self.settings_file = settings_file
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

    def get_setting(self, key, default=None):
        return self.settings.get(key, self.default_settings.get(key, default))


class SettingsSaver:
    def __init__(self, settings_loader):
        self.settings_loader = settings_loader

    def save_settings(self):
        with open(self.settings_loader.settings_file, 'w') as f:
            json.dump(self.settings_loader.settings, f, indent=4)

    def set_setting(self, key, value):
        self.settings_loader.settings[key] = value
        self.save_settings()


settings_loader = SettingsLoader()
settings_saver = SettingsSaver(settings_loader)

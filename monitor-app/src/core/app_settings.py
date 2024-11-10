import json
import os
import winreg

class SettingsLoader:
    def __init__(self, settings_file='settings.json'):
        self.settings_file = settings_file
        self.default_settings = {
            'webhook_url': '',
            'api_key': '',
            'steam_id': '',
            'check_interval': 10,
            'game_app_id': 892970,  # Valheim's App ID as default
            'monitor_mode': 'both',
            'auto_run': False
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


def set_auto_run(app_name, app_path):
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
        winreg.SetValueEx(reg_key, app_name, 0, winreg.REG_SZ, app_path)


def remove_auto_run(app_name):
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
        winreg.DeleteValue(reg_key, app_name)


settings_loader = SettingsLoader()
settings_saver = SettingsSaver(settings_loader)

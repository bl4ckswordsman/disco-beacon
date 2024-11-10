import json
import os
import sys
from src.gui.utils.platform_utils import is_windows
from src.core.logger import logger
from src.gui.utils.app_settings import AppSettings

if is_windows():
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
    if is_windows():
        # Use the actual exe path instead of the temporary pyc file
        if getattr(sys, 'frozen', False):
            exe_path = f'"{sys.executable}"'
        else:
            exe_path = f'"{os.path.abspath(app_path)}"'

        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, app_name, 0, winreg.REG_SZ, exe_path)
                # Verify the entry was set correctly
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_READ) as verify_key:
                    value, _ = winreg.QueryValueEx(verify_key, app_name)
                    if value != exe_path:
                        raise ValueError("Registry value verification failed")
        except Exception as e:
            logger.error(f"Failed to set autorun registry: {e}")
            settings_saver.set_setting('auto_run', False)


def remove_auto_run(app_name):
    if is_windows():
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.DeleteValue(reg_key, app_name)
        except FileNotFoundError:
            pass


def verify_auto_run(app_name):
    """Verify if the autorun registry entry exists and matches the current executable"""
    if not is_windows():
        return False

    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_READ) as reg_key:
            value, _ = winreg.QueryValueEx(reg_key, app_name)
            expected_path = f'"{sys.executable}"' if getattr(sys, 'frozen', False) else f'"{os.path.abspath(sys.argv[0])}"'
            return value == expected_path
    except (WindowsError, FileNotFoundError):
        return False

def sync_autorun_setting():
    """Synchronize the autorun setting with the actual registry state"""
    if is_windows():
        actual_autorun = verify_auto_run(AppSettings.APP_NAME)
        if settings_loader.get_setting('auto_run') != actual_autorun:
            settings_saver.set_setting('auto_run', actual_autorun)


settings_loader = SettingsLoader()
settings_saver = SettingsSaver(settings_loader)

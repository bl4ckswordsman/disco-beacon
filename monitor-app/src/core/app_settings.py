import json
import os
import sys
from src.gui.utils.platform_utils import is_windows
from src.core.logger import logger
from src.gui.utils.app_settings import AppSettings

if is_windows():
    import winreg

class SettingsLoader:
    def __init__(self):
        self.default_settings = {
            'webhook_url': '',
            'api_key': '',
            'steam_id': '',
            'check_interval': 10,
            'game_app_id': 892970,  # Valheim's App ID as default
            'monitor_mode': 'both',
            'auto_run': False
        }
        self.settings_file = self._get_settings_path()
        self.settings = self.load_settings()

    def _get_settings_path(self):
        """Get the appropriate settings file path based on the platform"""
        try:
            if is_windows():
                base_path = os.path.join(os.getenv('APPDATA', ''), AppSettings.ORG_NAME, AppSettings.APP_NAME)
            else:
                config_home = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
                base_path = os.path.join(config_home, 'disco-beacon')

            if not os.path.exists(base_path):
                old_umask = os.umask(0o077)
                try:
                    os.makedirs(base_path, mode=0o700, exist_ok=True)
                finally:
                    os.umask(old_umask)

            settings_path = os.path.join(base_path, 'settings.json')
            return settings_path
        except Exception as e:
            logger.error(f"Failed to get settings path: {e}")
            fallback_path = os.path.expanduser(f"~/.disco-beacon-settings.json")
            logger.info(f"Using fallback settings path: {fallback_path}")
            return fallback_path

    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    merged_settings = self.default_settings.copy()
                    merged_settings.update(loaded_settings)
                    return merged_settings
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
        return self.default_settings.copy()

    def get_setting(self, key, default=None):
        return self.settings.get(key, self.default_settings.get(key, default))

class SettingsSaver:
    def __init__(self, settings_loader):
        self.settings_loader = settings_loader

    def save_settings(self):
        temp_file = None
        old_umask = None
        try:
            old_umask = os.umask(0o077)
            settings_dir = os.path.dirname(self.settings_loader.settings_file)

            if not os.path.exists(settings_dir):
                os.makedirs(settings_dir, mode=0o700)

            temp_file = f"{self.settings_loader.settings_file}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(self.settings_loader.settings, f, indent=4)
                f.flush()
                os.fsync(f.fileno())

            os.chmod(temp_file, 0o600)
            os.replace(temp_file, self.settings_loader.settings_file)
            os.chmod(self.settings_loader.settings_file, 0o600)
            return True

        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            return False

        finally:
            if old_umask is not None:
                os.umask(old_umask)
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass

    def set_setting(self, key, value):
        self.settings_loader.settings[key] = value
        return self.save_settings()

def set_auto_run(app_name, app_path):
    """Set up autorun for Windows"""
    if not is_windows():
        return False

    try:
        exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(app_path)
        quoted_path = f'"{exe_path}"'

        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key) as reg_key:
            winreg.SetValueEx(reg_key, app_name, 0, winreg.REG_SZ, quoted_path)
            return True
    except Exception as e:
        logger.error(f"Failed to set autorun registry: {e}")
        return False

def remove_auto_run(app_name):
    """Remove autorun entry for Windows"""
    if not is_windows():
        return True

    try:
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.DeleteValue(reg_key, app_name)
        return True
    except FileNotFoundError:
        return True
    except Exception as e:
        logger.error(f"Failed to remove autorun registry: {e}")
        return False

def handle_autorun_change(enabled: bool):
    """Handle changes to autorun setting"""
    if not is_windows():
        return True

    app_name = AppSettings.APP_NAME
    app_path = os.path.abspath(sys.argv[0])

    if enabled:
        return set_auto_run(app_name, app_path)
    else:
        return remove_auto_run(app_name)

# Initialize singleton instances
settings_loader = SettingsLoader()
settings_saver = SettingsSaver(settings_loader)

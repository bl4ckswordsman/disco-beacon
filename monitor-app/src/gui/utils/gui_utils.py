import os
import time
import subprocess
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette
from src.gui.utils.gui_config import gui_config
from src.gui.utils.platform_utils import is_linux, is_windows
from src.core.logger import logger


def get_windows_theme():
    try:
        import winreg
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        ) as key:
            # AppsUseLightTheme = 0 means dark theme, 1 means light theme
            value = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
            return 'light' if value == 1 else 'dark'
    except Exception:
        return None


_cached_theme = None
_last_check_time = 0


def get_current_theme():
    """Get current theme with caching to avoid frequent system calls"""
    global _cached_theme, _last_check_time

    try:
        current_time = time.time()

        # Return cached theme if less than 5 seconds old
        if _cached_theme and current_time - _last_check_time < 5:
            return _cached_theme

        app = QApplication.instance()
        if not app:
            return 'light'

        theme = None

        # Try platform-specific detection first
        if is_windows():
            theme = get_windows_theme()
        elif is_linux():
            desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
            if desktop in ['gnome', 'unity']:
                try:
                    result = subprocess.run(
                        ['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'],
                        capture_output=True,
                        text=True,
                        timeout=1
                    )
                    theme = 'dark' if 'dark' in result.stdout.lower() else 'light'
                except (subprocess.SubprocessError, subprocess.TimeoutExpired):
                    pass

        # Fallback to Qt palette detection
        if not theme:
            palette = app.palette()
            window_color = palette.color(QPalette.ColorRole.Window)
            text_color = palette.color(QPalette.ColorRole.WindowText)
            theme = 'dark' if window_color.lightness() < text_color.lightness() else 'light'

        _cached_theme = theme
        _last_check_time = current_time
        return theme

    except Exception as e:
        logger.warning(f"Error detecting theme: {e}")
        return 'light'  # Default to light theme on error


def get_icon_path(theme: str) -> str:
    if is_linux():
        return f"{gui_config.ICON_THEME_DARK}/{gui_config.ICON_NAME}"
    icon_theme = gui_config.ICON_THEME_LIGHT if theme == 'light' else gui_config.ICON_THEME_DARK
    return f"{icon_theme}/{gui_config.ICON_NAME}"

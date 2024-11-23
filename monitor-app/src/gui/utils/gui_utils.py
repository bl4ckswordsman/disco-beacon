import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette
from src.gui.utils.gui_config import gui_config
from src.gui.utils.platform_utils import is_linux, is_windows


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

def get_current_theme():
    app = QApplication.instance()
    if not app:
        return 'light'  # Default to light theme if app instance is not available

    if is_windows():
        windows_theme = get_windows_theme()
        if windows_theme:
            return windows_theme

    if is_linux():
        # Try to detect system theme through environment variables
        desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
        if desktop in ['gnome', 'unity']:
            import subprocess
            try:
                result = subprocess.run(
                    ['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'],
                    capture_output=True,
                    text=True
                )
                if 'dark' in result.stdout.lower():
                    return 'dark'
                return 'light'
            except:
                pass

    # Fallback to Qt palette detection for all platforms
    palette = app.palette()
    window_color = palette.color(QPalette.ColorRole.Window)
    text_color = palette.color(QPalette.ColorRole.WindowText)
    return 'dark' if window_color.lightness() < text_color.lightness() else 'light'


def get_icon_path(theme: str) -> str:
    if is_linux():
        return f"{gui_config.ICON_THEME_DARK}/{gui_config.ICON_NAME}"
    icon_theme = gui_config.ICON_THEME_LIGHT if theme == 'light' else gui_config.ICON_THEME_DARK
    return f"{icon_theme}/{gui_config.ICON_NAME}"

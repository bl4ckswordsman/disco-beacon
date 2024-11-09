from win32mica import ApplyMica, MicaTheme, MicaStyle
from src.core.logger import logger
from src.gui.utils.gui_utils import get_current_theme

def apply_mica_to_window(window) -> bool:
    """
    Apply Mica effect to a Qt window using win32mica.

    Args:
        window: PySide6 window instance

    Returns:
        bool: True if successfully applied, False otherwise
    """
    try:
        if not window.winId():
            window.create()

        hwnd = window.winId().__int__()
        if not hwnd:
            logger.error("Failed to get window handle")
            return False

        # Set theme based on current system theme
        theme = MicaTheme.DARK if get_current_theme() == 'dark' else MicaTheme.LIGHT

        # Apply Mica effect with auto theme switching
        ApplyMica(
            HWND=hwnd,
            Theme=MicaTheme.AUTO,  # Auto-switch based on system theme
            Style=MicaStyle.DEFAULT,
            OnThemeChange=lambda new_theme: logger.debug(f"Mica theme changed to: {new_theme}")
        )
        return True

    except Exception as e:
        logger.error(f"Error applying Mica effect: {e}")
        return False

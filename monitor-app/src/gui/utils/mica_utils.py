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
        # Create window if it doesn't exist
        if not window.winId():
            window.create()
            window.show()  # Window needs to be visible for Mica effect

        hwnd = window.winId().__int__()
        if not hwnd:
            logger.error("Failed to get window handle")
            return False

        def theme_change_callback(new_theme):
            """Handle theme changes from system"""
            theme_name = "dark" if new_theme == MicaTheme.DARK else "light"
            logger.info(f"System theme changed to: {theme_name}")
            window.theme_changed.emit(theme_name)

        # Apply Mica effect with auto theme switching
        ApplyMica(
            HWND=hwnd,
            Theme=MicaTheme.AUTO,  # Auto-switch based on system theme
            Style=MicaStyle.DEFAULT,  # Use default style for better visibility
            OnThemeChange=theme_change_callback
        )

        logger.info("Successfully applied Mica effect")
        return True

    except ImportError as e:
        logger.error(f"win32mica import error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error applying Mica effect: {e}")
        return False

from PySide6.QtCore import Qt
from src.core.logger import logger
from src.gui.utils.platform_utils import is_windows_11

# Only import win32mica on Windows
if is_windows_11():
    try:
        from win32mica import ApplyMica, MicaTheme, MicaStyle
        MICA_AVAILABLE = True
    except ImportError:
        logger.warning("win32mica module not available")
        MICA_AVAILABLE = False
else:
    MICA_AVAILABLE = False

def apply_mica_to_window(window) -> bool:
    """
    Apply Mica effect to a Qt window using win32mica.
    On non-Windows platforms, this function does nothing.

    Args:
        window: PySide6 window instance

    Returns:
        bool: True if successfully applied or skipped, False if failed
    """
    if not is_windows_11() or not MICA_AVAILABLE:
        logger.debug("Mica effect not available on this platform")
        return True  # Return True since this is expected behavior

    try:
        # Enable translucent background for Mica effect (Windows 11 only)
        window.setAttribute(Qt.WA_TranslucentBackground)

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
            Style=MicaStyle.ALT,  # MicaStyle.DEFAULT or MicaStyle.ALT
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

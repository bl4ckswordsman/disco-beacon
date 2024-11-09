import ctypes
from enum import IntEnum
from src.core.logger import logger

class DwmWindowAttribute(IntEnum):
    """Windows 11 DWM window attributes"""
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    DWMWA_SYSTEMBACKDROP_TYPE = 38
    DWMWA_MICA_EFFECT = 1029

class DwmSystemBackdropType(IntEnum):
    """Windows 11 system backdrop types"""
    DWMSBT_AUTO = 0
    DWMSBT_NONE = 1
    DWMSBT_MAINWINDOW = 2
    DWMSBT_TRANSIENTWINDOW = 3
    DWMSBT_TABBEDWINDOW = 4

def apply_mica_effect(hwnd: int) -> bool:
    """
    Apply the Windows 11 Mica effect to a window.

    Args:
        hwnd: Window handle to apply the effect to

    Returns:
        bool: True if successfully applied, False otherwise
    """
    try:
        dwm = ctypes.WinDLL("dwmapi")

        # Try the newer Windows 11 22H2+ method first (preferred)
        try:
            success = _set_window_attribute(
                dwm,
                hwnd,
                DwmWindowAttribute.DWMWA_SYSTEMBACKDROP_TYPE,
                DwmSystemBackdropType.DWMSBT_MAINWINDOW
            )
            if success:
                return True
        except Exception:
            logger.debug("Windows 11 22H2+ method failed, trying fallback")

        # Fallback for earlier Windows 11 versions
        try:
            success = _set_window_attribute(
                dwm,
                hwnd,
                DwmWindowAttribute.DWMWA_MICA_EFFECT,
                True
            )
            if success:
                return True
        except Exception:
            logger.debug("Windows 11 fallback method failed")

        return False

    except Exception as e:
        logger.error(f"Failed to apply Mica effect: {e}")
        return False

def _set_window_attribute(dwm, hwnd: int, attribute: DwmWindowAttribute, value: int) -> bool:
    """Helper function to set DWM window attributes"""
    val = ctypes.c_int(value)
    result = dwm.DwmSetWindowAttribute(
        hwnd,
        attribute,
        ctypes.byref(val),
        ctypes.sizeof(val)
    )
    if result != 0:  # S_OK = 0
        raise OSError(f"DwmSetWindowAttribute failed with code {result}")
    return True

def apply_mica_to_window(window) -> bool:
    """
    Apply Mica effect to a Qt window.

    Args:
        window: PySide6 window instance

    Returns:
        bool: True if successfully applied, False otherwise
    """
    try:
        if not window.winId():
            window.create()

        hwnd = int(window.winId())
        if not hwnd:
            logger.error("Failed to get window handle")
            return False

        return apply_mica_effect(hwnd)

    except Exception as e:
        logger.error(f"Error applying Mica effect: {e}")
        return False

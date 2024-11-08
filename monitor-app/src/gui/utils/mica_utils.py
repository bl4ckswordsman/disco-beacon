import ctypes
from ctypes import wintypes
from PySide6.QtCore import Qt

class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ('AccentState', ctypes.c_uint),
        ('AccentFlags', ctypes.c_uint),
        ('GradientColor', ctypes.c_uint),
        ('AnimationId', ctypes.c_uint)
    ]

class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ('Attribute', ctypes.c_uint),
        ('Data', ctypes.POINTER(ACCENT_POLICY)),
        ('SizeOfData', ctypes.c_size_t)
    ]

class DWM_SYSTEMBACKDROP_TYPE(ctypes.c_int):
    DWMSBT_AUTO = 0
    DWMSBT_NONE = 1
    DWMSBT_MAINWINDOW = 2
    DWMSBT_TRANSIENTWINDOW = 3
    DWMSBT_TABBEDWINDOW = 4

def apply_mica_effect(hwnd):
    """Apply the Windows 11 Mica effect to a window."""
    try:
        # Load dwmapi.dll
        dwm = ctypes.WinDLL("dwmapi")

        # Try to use DWM_SYSTEMBACKDROP_TYPE (Windows 11 22H2 and later)
        try:
            set_backdrop = dwm.DwmSetWindowAttribute
            backdrop_type = DWM_SYSTEMBACKDROP_TYPE.DWMSBT_MAINWINDOW
            set_backdrop(
                hwnd,
                35,  # DWMWA_SYSTEMBACKDROP_TYPE
                ctypes.byref(ctypes.c_int(backdrop_type)),
                ctypes.sizeof(ctypes.c_int)
            )
            return True
        except Exception:
            # Fallback for earlier Windows 11 versions
            DWMWA_MICA_EFFECT = 1029
            set_mica = dwm.DwmSetWindowAttribute
            value = ctypes.c_int(1)
            set_mica(
                hwnd,
                DWMWA_MICA_EFFECT,
                ctypes.byref(value),
                ctypes.sizeof(value)
            )
            return True

    except Exception as e:
        print(f"Failed to apply Mica effect: {e}")
        return False

def apply_mica_to_window(window):
    """Apply Mica effect to a Qt window."""
    try:
        # Make sure the window is created
        window.create()

        # Get the window handle
        hwnd = window.winId()

        # Apply the effect
        success = apply_mica_effect(int(hwnd))

        if success:
            # Additional Qt window settings for proper transparency
            window.setAttribute(Qt.WA_TranslucentBackground)
            window.setStyleSheet("background: transparent;")

        return success
    except Exception as e:
        print(f"Error applying Mica effect: {e}")
        return False

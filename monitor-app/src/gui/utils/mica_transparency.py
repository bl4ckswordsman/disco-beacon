import ctypes
from ctypes import wintypes

class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ('AccentState', ctypes.c_int),
        ('AccentFlags', ctypes.c_int),
        ('GradientColor', ctypes.c_int),
        ('AnimationId', ctypes.c_int)
    ]

class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ('Attribute', ctypes.c_int),
        ('Data', ctypes.POINTER(ACCENT_POLICY)),
        ('SizeOfData', ctypes.c_size_t)
    ]

WCA_ACCENT_POLICY = 19
ACCENT_ENABLE_BLURBEHIND = 3

def enable_mica_transparency():
    accent_policy = ACCENT_POLICY()
    accent_policy.AccentState = ACCENT_ENABLE_BLURBEHIND
    accent_policy.GradientColor = 0x00FFFFFF  # White with full transparency

    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = WCA_ACCENT_POLICY
    data.Data = ctypes.pointer(accent_policy)
    data.SizeOfData = ctypes.sizeof(accent_policy)

    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))

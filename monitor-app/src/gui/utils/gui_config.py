from PySide6.QtCore import Qt

class GUIConfig:
    WINDOW_WIDTH: int = 600
    WINDOW_HEIGHT: int = 400
    GUI_REFRESH_RATE: int = 1000  # ms

    FONT_FAMILY: str = 'Helvetica'
    FONT_SIZE_NORMAL: int = 12
    FONT_SIZE_LARGE: int = 18
    SETTINGS_BUTTON_SIZE: int = 20
    SETTINGS_BUTTON_FONT_SIZE: int = 14
    ICON_THEME_LIGHT: str = ':/icons/light'
    ICON_THEME_DARK: str = ':/icons/dark'
    ICON_NAME: str = 'tower-control.svg'
    WINDOW_ICON_PNG: str = ':/icons/tower-control.png'
    WINDOW_ICON: str = ':/icons/tower-control.ico'

    COLORS = {
        'light': {
            'background': Qt.white,
            'text': Qt.black,
            'accent': Qt.blue,
            'online': Qt.green,
            'offline': Qt.red
        },
        'dark': {
            'background': Qt.darkGray,
            'text': Qt.white,
            'accent': Qt.cyan,
            'online': Qt.green,
            'offline': Qt.red
        }
    }


gui_config = GUIConfig()

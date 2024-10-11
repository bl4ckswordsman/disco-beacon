from PySide6.QtCore import Qt

class GUIConfig:
    WINDOW_WIDTH: int = 800
    WINDOW_HEIGHT: int = 600
    GUI_REFRESH_RATE: int = 1000  # ms

    FONT_FAMILY: str = 'Arial'
    FONT_SIZE_NORMAL: int = 12
    FONT_SIZE_LARGE: int = 16
    ICON_THEME_LIGHT: str = ':/icons/light'
    ICON_THEME_DARK: str = ':/icons/dark'
    ICON_NAME: str = 'tower-control.svg'
    WINDOW_ICON: str = ':/icons/tower-control.ico'

    COLORS = {
        'background': Qt.white,
        'text': Qt.black,
        'accent': Qt.blue,
        'online': Qt.green,
        'offline': Qt.red
    }


gui_config = GUIConfig()

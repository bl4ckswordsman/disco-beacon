from PySide6.QtWidgets import QApplication
import sys
from src.gui.mainwindow import MainWindow
from src.gui.system_tray import SystemTrayIcon
from src.core.logger import logger
import resources.resources # noqa: F401
from src.gui.utils.gui_utils import get_current_theme
from PySide6.QtCore import QOperatingSystemVersion
from src.gui.utils.mica_transparency import enable_mica_transparency

def init_gui():
    # import os
    # os.environ['QT_QPA_PLATFORM'] = 'xcb'  # Platform: xcb | wayland
    # os.environ['QT_STYLE_OVERRIDE'] = 'Fusion'  # Style: Fusion| Windows
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Explicitly set Fusion style
    window = MainWindow()
    current_theme = get_current_theme()
    tray_icon = SystemTrayIcon(window, theme=current_theme)
    tray_icon.show()

    # Connect tray icon's exit signal to a function that will quit the application
    tray_icon.exit_app.connect(lambda: (app.quit(), sys.exit(0)))

    window.show()

    # Set the tray icon for the main window
    window.set_tray_icon(tray_icon)

    if QOperatingSystemVersion.current() == QOperatingSystemVersion.Windows11:
        enable_mica_transparency()

    logger.info("GUI initialized with system tray icon and Fusion style")
    return app, window, tray_icon

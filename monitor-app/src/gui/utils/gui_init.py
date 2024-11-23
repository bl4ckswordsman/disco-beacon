from PySide6.QtWidgets import QApplication
import sys
from src.gui.mainwindow import MainWindow
from src.gui.system_tray import SystemTrayIcon
from src.core.logger import logger
import resources.resources # noqa: F401
from src.gui.utils.gui_utils import get_current_theme
from src.gui.utils.platform_utils import is_windows_11
from src.gui.utils.mica_utils import apply_mica_to_window
from src.gui.utils.platform_utils import is_linux

def init_gui():
    """Initialize the GUI application with appropriate platform-specific settings."""
    import os

    # Set environment variables for Linux theme support
    if is_linux():
        os.environ['QT_QPA_PLATFORMTHEME'] = 'qt6ct'  # Use qt6ct for theme management
        os.environ['QT_STYLE_OVERRIDE'] = 'Fusion'
        # Suppress GTK module warnings
        # os.environ['NO_AT_BRIDGE'] = '1'
    # import os
    # os.environ['QT_QPA_PLATFORM'] = 'xcb'  # Platform: xcb | wayland
    # os.environ['QT_STYLE_OVERRIDE'] = 'Fusion'  # Style: Fusion| Windows

    # Initialize application
    app = QApplication(sys.argv)

    if not is_windows_11():
        app.setStyle("Fusion")  # Use Fusion style on non-Windows platforms

    window = MainWindow()

    if is_windows_11():
        apply_mica_to_window(window)

    # Setup system tray
    current_theme = get_current_theme()
    tray_icon = SystemTrayIcon(window, theme=current_theme)
    tray_icon.show()

    # Connect tray icon's exit signal to a function that will quit the application
    tray_icon.exit_app.connect(lambda: (app.quit(), sys.exit(0)))

    window.show()

    # Set the tray icon for the main window
    window.set_tray_icon(tray_icon)

    logger.info("GUI initialized with system tray icon and Fusion style")
    return app, window, tray_icon

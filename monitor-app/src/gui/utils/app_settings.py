from PySide6.QtGui import QIcon
from PySide6.QtCore import QCoreApplication

class AppSettings:
    APP_NAME = "Disco Beacon"
    APP_ID = "com.bl4ckswordsman"
    ICON_PATH = ":/icons/light/tower-control.svg"

    @classmethod
    def set_app_metadata(cls):
        QCoreApplication.setApplicationName(cls.APP_NAME)
        QCoreApplication.setOrganizationName("bl4ckswordsman")
        QCoreApplication.setApplicationVersion("0.0.1")
        QCoreApplication.setOrganizationDomain("bl4ckswordsman.com")

    @classmethod
    def get_app_icon(cls):
        return QIcon(cls.ICON_PATH)

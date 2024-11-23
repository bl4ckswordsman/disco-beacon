from PySide6.QtCore import QCoreApplication
from src.version import __version__


class AppSettings:
    APP_NAME = "Disco Beacon"
    ORG_NAME = "bl4ckswordsman"
    APP_ID = "com." + ORG_NAME
    ORG_DOMAIN = ORG_NAME + ".com"
    ICON_PATH = ":/icons/light/tower-control.svg"
    VERSION = __version__.lstrip('v')

    @classmethod
    def set_app_metadata(cls):
        QCoreApplication.setApplicationName(cls.APP_NAME)
        QCoreApplication.setOrganizationName(cls.ORG_NAME)
        QCoreApplication.setApplicationVersion(cls.VERSION)
        QCoreApplication.setOrganizationDomain(cls.ORG_DOMAIN)

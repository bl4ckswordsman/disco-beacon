import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from main import main
from src.core.single_instance import SingleInstance
from src.core.logger import logger

if __name__ == "__main__":
    with SingleInstance("/tmp/disco_beacon.lock") as instance:
        if not instance:
            logger.error("Another instance of the application is already running.")
            sys.exit(1)
        main()

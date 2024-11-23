import os

if os.name == 'nt':
    import msvcrt
else:
    import fcntl

from src.core.logger import logger

import tempfile

class SingleInstance:
    def __init__(self):
        self.fp = None
        if os.name == 'nt':
            self.lockfile = os.path.join(tempfile.gettempdir(), 'disco_beacon.lock')
        else:
            self.lockfile = '/tmp/disco_beacon.lock'

    def __enter__(self):
        try:
            os.makedirs(os.path.dirname(self.lockfile), exist_ok=True)
            self.fp = open(self.lockfile, 'w')
            try:
                if os.name == 'nt':
                    msvcrt.locking(self.fp.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    fcntl.flock(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except (IOError, OSError):
                self.fp.close()
                return False
            return True
        except Exception as e:
            logger.error(f"Error creating lock file: {e}")
            return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.fp:
                if os.name == 'nt':
                    msvcrt.locking(self.fp.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(self.fp, fcntl.LOCK_UN)
                self.fp.close()
                try:
                    os.remove(self.lockfile)
                except FileNotFoundError:
                    pass
        except Exception as e:
            logger.error(f"Error cleaning up lock file: {e}")

import os
import tempfile
from contextlib import contextmanager
from src.core.logger import logger

if os.name == 'nt':
    import msvcrt
else:
    import fcntl

class SingleInstance:
    def __init__(self):
        self.lockfile = os.path.join(tempfile.gettempdir(), 'disco_beacon.lock')
        self.fp = None

    @contextmanager
    def get_lock(self):
        try:
            os.makedirs(os.path.dirname(self.lockfile), exist_ok=True)
            self.fp = open(self.lockfile, 'w')

            try:
                if os.name == 'nt':
                    msvcrt.locking(self.fp.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    fcntl.flock(self.fp, fcntl.LOCK_EX | fcntl.LOCK_NB)

                # Write PID for debugging purposes
                self.fp.write(str(os.getpid()))
                self.fp.flush()
                yield True

            except (IOError, OSError):
                self.fp.close()
                self.fp = None
                yield False

        except Exception as e:
            logger.error(f"Error with lock file: {e}")
            if self.fp:
                self.fp.close()
                self.fp = None
            yield False

        finally:
            if self.fp:
                try:
                    if os.name == 'nt':
                        msvcrt.locking(self.fp.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        fcntl.flock(self.fp, fcntl.LOCK_UN)
                    self.fp.close()
                    os.remove(self.lockfile)
                except Exception as e:
                    logger.error(f"Error cleaning up lock file: {e}")
                self.fp = None

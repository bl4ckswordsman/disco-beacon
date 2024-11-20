import os
import sys

if os.name == 'nt':
    import msvcrt
else:
    import fcntl

class SingleInstance:
    def __init__(self, lockfile):
        self.lockfile = lockfile
        self.fp = None

    def __enter__(self):
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

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if os.name == 'nt':
                msvcrt.locking(self.fp.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(self.fp, fcntl.LOCK_UN)
        finally:
            self.fp.close()
            os.remove(self.lockfile)

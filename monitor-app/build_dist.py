import os
import shutil
import subprocess
import sys
from version import __version__

def build_executable():
    subprocess.run(["pyinstaller", "--clean", "disco_beacon.spec"], check=True)

def copy_additional_files():
    shutil.copy("settings.json", os.path.join("dist", "DiscoBeacon"))

def create_archive():
    archive_format = "zip" if sys.platform == "win32" else "gztar"
    platform = "Windows" if sys.platform == "win32" else "Linux"
    archive_name = f"DiscoBeacon_{platform}_{__version__}"
    shutil.make_archive(archive_name, archive_format, os.path.join("dist", "DiscoBeacon"))
    return f"{archive_name}.{'zip' if sys.platform == 'win32' else 'tar.gz'}"

if __name__ == "__main__":
    build_executable()
    copy_additional_files()
    archive_path = create_archive()
    print(f"Distribution package created: {archive_path}")

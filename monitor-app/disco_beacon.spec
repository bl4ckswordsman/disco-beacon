# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# Get the absolute path of the current script
script_path = os.path.dirname(os.path.abspath(SPECPATH))

# Read version from version.py
version_path = os.path.join(script_path, 'version.py')
version_string = "0.0.1"  # Default version if file not found
if os.path.exists(version_path):
    with open(version_path, 'r') as f:
        exec(f.read())
    version_string = locals().get('__version__', version_string)

a = Analysis(
    ['main.py'],
    pathex=[script_path],
    binaries=[],
    datas=[('resources', 'resources'), ('version.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DiscoBeacon',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=version_string,
    icon=['resources/icons/light/tower-control.svg'],
)

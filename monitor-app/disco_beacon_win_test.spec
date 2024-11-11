# -*- mode: python ; coding: utf-8 -*-

import os

# Toggle debug mode here
DEBUG_MODE = True  # Set to True to enable console and use main.py

block_cipher = None

# Define the paths
icons_dir = 'icons'
ico_icon_path = os.path.join('icons', 'tower-control.ico')

# Select main file based on debug mode
main_file = 'main.py' if DEBUG_MODE else 'windows_main.pyw'

a = Analysis(
    [main_file],  # Use the selected main file
    pathex=[],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        (icons_dir, 'icons'),  # Include the entire icons directory
    ],
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
    version_file=None,  # Version info from version.py will be shown in the app
    debug=DEBUG_MODE,  # Set debug based on DEBUG_MODE
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=DEBUG_MODE,  # Set console based on DEBUG_MODE
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[ico_icon_path],
)

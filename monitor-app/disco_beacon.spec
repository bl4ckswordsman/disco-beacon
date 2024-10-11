# -*- mode: python ; coding: utf-8 -*-

import sys
import os
import platform

block_cipher = None

# Define the correct path to your icon files
svg_icon_path = os.path.join('icons', 'light', 'tower-control.svg')
ico_icon_path = os.path.join('icons', 'tower-control.ico')
icons_dir = 'icons'

a = Analysis(
    ['main.py'],
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
    [],
    exclude_binaries=True,
    name='DiscoBeacon',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[ico_icon_path] if sys.platform == 'win32' else [svg_icon_path],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DiscoBeacon',
)

if platform.system() == "Windows":
    a_windows = Analysis(
        ['windows_main.pyw'],
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

    pyz_windows = PYZ(a_windows.pure, a_windows.zipped_data, cipher=block_cipher)

    exe_windows = EXE(
        pyz_windows,
        a_windows.scripts,
        [],
        exclude_binaries=True,
        name='DiscoBeacon',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=[ico_icon_path],
    )

    coll_windows = COLLECT(
        exe_windows,
        a_windows.binaries,
        a_windows.zipfiles,
        a_windows.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name='DiscoBeacon',
    )

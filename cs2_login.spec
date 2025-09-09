# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Get the base directory
base_dir = os.path.abspath(os.path.dirname(SPECPATH))

# Collect all necessary data files
assets_dir = os.path.join(base_dir, 'app', 'assets')
assets = []
for root, dirs, files in os.walk(assets_dir):
    for file in files:
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, base_dir)
        target_path = os.path.dirname(rel_path)
        assets.append((file_path, target_path))

# Add .env file if it exists
env_file = os.path.join(base_dir, '.env')
if os.path.exists(env_file):
    assets.append((env_file, '.'))

# Collect all necessary modules
hidden_imports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.QtWebEngineWidgets',
    'PyQt6.QtWebEngineCore',
    'supabase',
    'dotenv',
    'keyring',
    'cryptography'
] + collect_submodules('supabase')

a = Analysis(
    ['main.py'],
    pathex=[base_dir],
    binaries=[],
    datas=assets,
    hiddenimports=hidden_imports,
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
    name='CS2_Tool_Login',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(base_dir, 'app', 'assets', 'icons', 'app_icon.ico') if os.path.exists(os.path.join(base_dir, 'app', 'assets', 'icons', 'app_icon.ico')) else None,
)
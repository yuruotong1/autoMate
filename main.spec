# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for autoMate — works on Windows, macOS and Linux.

Build command:
    pyinstaller main.spec --noconfirm
"""
import sys
import os
from PyInstaller.utils.hooks import collect_data_files

# ---------------------------------------------------------------------------
# Project root (directory containing this spec file)
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.abspath(SPEC))

# ---------------------------------------------------------------------------
# Data files to bundle
# ---------------------------------------------------------------------------
datas = []
datas += collect_data_files('gradio_client')
datas += collect_data_files('gradio')
datas += collect_data_files('safehttpx')
datas += collect_data_files('groovy')

imgs_path = os.path.join(ROOT, 'imgs')
if os.path.exists(imgs_path):
    datas += [(imgs_path, 'imgs')]

# ---------------------------------------------------------------------------
# Hidden imports that PyInstaller static analysis may miss
# ---------------------------------------------------------------------------
hidden_imports = [
    # PyQt6
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.sip',
    # Vision / ML
    'cv2',
    'supervision',
    'ultralytics',
    'timm',
    'einops',
    # LLM clients
    'anthropic',
    'openai',
    'openai.types',
    'openai._models',
    'mcp',
    'mcp.server',
    'mcp.server.fastmcp',
    # Automation
    'pyautogui',
    'pyperclip',
    'keyboard',
    'pynput',
    'pynput.keyboard',
    'pynput.mouse',
    # Model download
    'modelscope',
    # Utilities
    'pydantic',
    'PIL',
    'PIL.Image',
    'numpy',
]

# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
a = Analysis(
    ['main.py'],
    pathex=[ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy unused packages to reduce bundle size
        'IPython',
        'jupyter',
        'matplotlib',
        'scipy',
        'sklearn',
        'tensorflow',
        'pytest',
    ],
    noarchive=False,
    optimize=0,
    module_collection_mode={
        'gradio': 'py',
    },
)

pyz = PYZ(a.pure)

# ---------------------------------------------------------------------------
# Platform-specific settings
# ---------------------------------------------------------------------------
IS_WINDOWS = sys.platform == 'win32'
IS_MACOS   = sys.platform == 'darwin'

# Icon paths (optional — build succeeds even if these files are missing)
_ico  = os.path.join(ROOT, 'imgs', 'logo.ico')   # Windows
_icns = os.path.join(ROOT, 'imgs', 'logo.icns')  # macOS

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='autoMate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,           # UPX disabled — avoids AV false-positives on Windows
    console=not IS_WINDOWS,  # GUI-only on Windows; keep console on macOS/Linux
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=_ico if IS_WINDOWS and os.path.exists(_ico) else (
         _icns if IS_MACOS and os.path.exists(_icns) else None
    ),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='autoMate',
)

# ---------------------------------------------------------------------------
# macOS: wrap in a .app bundle (double-clickable)
# ---------------------------------------------------------------------------
if IS_MACOS:
    app = BUNDLE(
        coll,
        name='autoMate.app',
        icon=_icns if os.path.exists(_icns) else None,
        bundle_identifier='com.automate.desktop',
        info_plist={
            'NSHighResolutionCapable': True,
            'NSRequiresAquaSystemAppearance': False,  # support dark-mode
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleName': 'autoMate',
            # Accessibility + Screen Recording permissions
            'NSAccessibilityUsageDescription': 'autoMate needs accessibility access to control the desktop.',
            'NSScreenCaptureDescription': 'autoMate needs screen recording access to take screenshots.',
        },
    )

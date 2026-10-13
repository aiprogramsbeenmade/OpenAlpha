# -*- mode: python ; coding: utf-8 -*-
"""
File di build per PyInstaller.

Genera un bundle self-contained di OpenAlpha per macOS, Windows, Linux.

Costruzione:
    pyinstaller openalpha.spec

Output:
    - macOS:   dist/OpenAlpha.app
    - Windows: dist/OpenAlpha.exe
    - Linux:   dist/OpenAlpha

Note:
    - Il bundle include Python e tutte le dipendenze.
    - I file statici (MathJax, Plotly, CSS, JS) sono inclusi come dati.
    - Su macOS, il bundle va autorizzato al primo avvio (Gatekeeper).
"""

import sys

# File statici e template da includere nel bundle.
datas = [
    ("openalpha/web/templates", "openalpha/web/templates"),
    ("openalpha/web/static", "openalpha/web/static"),
]

# Moduli nascosti (PyInstaller potrebbe non trovarli automaticamente).
hiddenimports = [
    "openalpha.operations",
    "openalpha.operations.algebra",
    "openalpha.operations.calculus",
    "openalpha.operations.equations",
    "openalpha.operations.numeric",
    "openalpha.operations.visualization",
    "openalpha.explanations",
    "openalpha.parser",
]

block_cipher = None


a = Analysis(
    ["openalpha/web/launcher.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name="OpenAlpha",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch="x86_64",
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="OpenAlpha",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="OpenAlpha.app",
        icon=None,
        bundle_identifier="com.openalpha.app",
        info_plist={
            "NSHighResolutionCapable": True,
            "LSMinimumSystemVersion": "10.15",
            "CFBundleDisplayName": "OpenAlpha",
            "CFBundleShortVersionString": "0.1.0",
        },
    )
# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for a PyQt/PySide app that uses styles/theme.qss
# Build with:  pyinstaller --clean main.spec
# (Do NOT run "pyinstaller main.py" - that overwrites this file.)


a = Analysis(
    ['main.py'],                 # your entry script
    pathex=[],
    binaries=[],
    datas=[
        # (source on your PC, relative to this .spec)  ->  (folder inside the exe)
        ('styles/theme.qss', 'styles'),

        # If your QSS uses images via url(...), bundle the whole folder instead:
        # ('styles', 'styles'),
        # ('assets', 'assets'),
    ],
    hiddenimports=[],            # add only if the exe shows "ModuleNotFoundError: No module named 'x'"
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

# Single-file exe (everything packed into one main.exe in dist/)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',                 # name of the generated exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,                # True while testing (shows errors); set False for the final build
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='assets/app.ico',     # optional: your app icon (.ico on Windows)
)

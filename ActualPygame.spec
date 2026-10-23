# -*- mode: python ; coding: utf-8 -*-


from pathlib import Path
project = Path(SPECPATH)

a = Analysis(
    [str(project / 'launch.py')],
    pathex=[str(project)],
    binaries=[],
    datas=[(str(project / 'assets'), 'assets'), (str(project / 'audio'), 'audio'), (str(project / 'UI'), 'UI'), (str(project / 'birdani'), 'birdani'), (str(project / 'mushrooms'), 'mushrooms'), (str(project / 'misks'), 'misks'), (str(project / 'asset-manifest.json'), '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ActualPygame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

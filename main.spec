# -*- mode: python ; coding: utf-8 -*-  # noqa: UP009, D100

import argparse

from PyInstaller.building.api import COLLECT, EXE, PYZ
from PyInstaller.building.build_main import Analysis

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true")
options = parser.parse_args()

EXE_NAME = "chilly-bird"


a = Analysis(
    scripts=["main.py"],
    pathex=[],
    binaries=[],
    datas=[("assets", "assets"), ("conf", "conf")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

if options.debug:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=EXE_NAME,
        debug=True,
        upx=True,
        console=True,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        upx=True,
        upx_exclude=[],
        name=EXE_NAME,
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name=EXE_NAME,
        debug=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        icon="assets\\img\\icons\\game.icon.png",
    )

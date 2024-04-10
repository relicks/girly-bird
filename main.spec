"""PyInstaller based builder."""

import argparse

from PyInstaller.building.api import COLLECT, EXE, PYZ
from PyInstaller.building.build_main import Analysis

parser = argparse.ArgumentParser(prog="PyInstaller based builder")
parser.add_argument(
    "build", choices=["debug", "release", "release-single-file"], default="debug"
)
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

match options.build:
    case "debug":
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
    case "release":
        exe = EXE(
            pyz,
            a.scripts,
            [],
            exclude_binaries=True,
            name=EXE_NAME,
            debug=False,
            upx=True,
            console=False,
            icon="assets\\img\\icons\\game.icon.png",
        )
        coll = COLLECT(
            exe,
            a.binaries,
            a.datas,
            upx=True,
            upx_exclude=[],
            name=EXE_NAME,
        )
    case "release-single-file":
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

# if options.debug:
#     exe = EXE(
#         pyz,
#         a.scripts,
#         [],
#         exclude_binaries=True,
#         name=EXE_NAME,
#         debug=True,
#         upx=True,
#         console=True,
#     )
#     coll = COLLECT(
#         exe,
#         a.binaries,
#         a.datas,
#         upx=True,
#         upx_exclude=[],
#         name=EXE_NAME,
#     )
# else:
# exe = EXE(
#     pyz,
#     a.scripts,
#     a.binaries,
#     a.datas,
#     [],
#     name=EXE_NAME,
#     debug=False,
#     upx=True,
#     upx_exclude=[],
#     runtime_tmpdir=None,
#     console=False,
#     icon="assets\\img\\icons\\game.icon.png",
# )

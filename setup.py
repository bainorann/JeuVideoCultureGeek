import os
import sys

from setuptools import setup

txt_files = [f for f in os.listdir(".") if f.endswith(".txt")]

APP = ["game.py"]
APP_NAME = "CultureGeekGame"

DATA_FILES = [
    ("", txt_files),
    ("assets/fonts", ["assets/fonts/DejaVuSansMono.ttf"]),
    (
        "assets/music",
        [
            "assets/music/prise de drogue.wav",
            "assets/music/soul à la plage.wav",
            "assets/music/tks_for_playing_KLICKAUD.mp3",
        ],
    ),
]

OPTIONS = {
    "argv_emulation": True,
    "packages": ["pygame"],
    "includes": [
        "display",
        "map",
        "player",
        "screen",
        "input_handler",
        "fight",
        "shop",
        "bank",
        "lasminas",
        "dialogue",
        "enemies",
        "item",
        "pages",
        "comeback",
        "tests",
        "tests.test11",
        "tests.helpers",
        "tests.layouts",
        "tests.layouts_2",
    ],
    "excludes": [
        "tkinter",
        "unittest",
        "email",
        "http",
        "urllib",
        "xml",
        "pydoc",
        "doctest",
        "pickle",
        "zipfile",
        "tarfile",
        "bz2",
        "lzma",
        "asyncio",
        "multiprocessing",
        "concurrent",
        "distutils",
        "lib2to3",
        "venv",
        "ensurepip",
        "curses",
        "dbm",
        "nntplib",
        "imaplib",
        "telnetlib",
        "smtplib",
        "poplib",
        "mailcap",
        "uu",
        "xdrlib",
        "nis",
        "ossaudiodev",
        "sndhdr",
        "msilib",
        "config-3",
        "test",
    ],
    "plist": {
        "NSHighResolutionCapable": True,
    },
}

setup(
    app=APP,
    name=APP_NAME,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)

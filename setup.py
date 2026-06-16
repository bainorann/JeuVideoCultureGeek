import sys

from cx_Freeze import Executable, setup

build_exe_options = {
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
        "tests",
        "tests.layouts",
        "tests.layouts_2",
    ],
    "include_files": [
        ("assets/fonts/DejaVuSansMono.ttf", "assets/fonts/DejaVuSansMono.ttf"),
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
        "distutils",
        "config-3",
        "test",
    ],
}

bdist_mac_options = {
    "iconfile": None,
    "bundle_name": "CultureGeekGame",
    "custom_info_plist": """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>""",
}

setup(
    name="CultureGeekGame",
    version="1.0",
    description="Jeu Video Culture Geek",
    options={
        "build_exe": build_exe_options,
        "bdist_mac": bdist_mac_options,
    },
    executables=[
        Executable(
            "game.py",
            base=None,
            target_name="CultureGeekGame",
        ),
    ],
)

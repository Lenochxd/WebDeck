import sys, os, json
from cx_Freeze import setup, Executable

with open('static/files/version.json', 'r', encoding="utf-8") as f:
    json_file = json.load(f)
    version = json_file['version']
    
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    # "excludes": ["tkinter", "unittest"],
    # "zip_include_packages": ["encodings", "PySide6"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="WebDeck",
    version=f"{version}",
    description="its free!",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)],
)
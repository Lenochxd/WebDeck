from cx_Freeze import setup, Executable
# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys, os
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    # tray icon
    Executable('main.py', base=base, target_name='WebDeck', icon='static/files/icon.ico'),
    # actual code
    Executable('main_server.py', base=base, target_name='WB_main')
    # bishokus.fr/webdeck/start
    Executable('start_server.py', base=base, target_name='WD_start')
]

with open('static/files/version.json', encoding="utf-8") as f:
    version = json.load(f)['actual_version']

setup(name='WebDeck',
    version = version,
    description = version,
    options = {'build_exe': build_options},
    executables = executables)

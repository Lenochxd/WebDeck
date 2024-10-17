import ctypes
import sys
import json
import os.path
import time
import threading

def load_config():
    for path in ['.config/config.json', 'config.json', 'webdeck/config_default.json']:
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                return json.load(f).get('settings', {})
    return {}

settings = load_config()

if settings['app_admin']:
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

from app.utils.is_opened import is_opened
from app.utils.global_variables import set_global_variable
import app.utils.languages as languages


def run_server_thread():
    from app.server import run_server
    run_server()

def initialize_tray_icon():
    from app.tray import create_tray_icon
    create_tray_icon()


if not is_opened():
    languages.init(
        lang_files_directory="webdeck/translations",
        default_language=settings['language']
    )
    threading.Thread(target=run_server_thread, daemon=True).start()
    initialize_tray_icon()
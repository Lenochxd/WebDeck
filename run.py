import ctypes
import sys
import json
import os.path
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

from app.utils.show_error import show_error
from app.utils.is_opened import is_opened
import app.utils.languages as languages


def run_server_thread():
    from app.server import run_server
    try:
        run_server()
    except Exception as e:
        show_error(exception=e)

def initialize_tray_icon():
    from app.tray import create_tray_icon
    try:
        create_tray_icon()
    except Exception as e:
        show_error(exception=e)


if not is_opened():
    languages.init(
        lang_files_directory="webdeck/translations",
        default_language=settings['language']
    )
    threading.Thread(target=run_server_thread, daemon=True).start()
    initialize_tray_icon()
import ctypes
import sys
import json
import os.path

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

import threading
from app.utils.is_opened import is_opened


if not is_opened():
    import app.utils.languages as languages
    from app.tray import create_tray_icon
    languages.init(
        lang_files_directory="webdeck/translations",
        default_language=settings['language']
    )

    def run_server_thread():
        from app.server import run_server
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()

    threading.Timer(0, run_server_thread).start()
    create_tray_icon()
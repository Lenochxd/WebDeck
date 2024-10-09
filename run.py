import ctypes
import sys
import json
import os.path

def load_config():
    for path in ['.config/config.json', 'config.json']:
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                return json.load(f).get('settings', {})
    return {}

try:
    settings = load_config()
    settings.setdefault('app_admin', True)
except Exception:
    settings = {'app_admin': True}

if settings['app_admin']:
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

import threading
from app.utils.is_opened import is_opened


if not is_opened():
    from app.server import run_server
    from app.tray import create_tray_icon
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    
    create_tray_icon()
    
    thread.join()
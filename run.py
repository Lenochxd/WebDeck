import ctypes
import sys
import json
import os.path

try:
    if os.path.exists('.config/config.json'):
        with open('.config/config.json', encoding='utf-8') as f:
            config = json.load(f)
            settings = config.get('settings', {})
    elif os.path.exists('config.json'):
        with open('config.json', encoding='utf-8') as f:
            config = json.load(f)
            settings = config.get('settings', {})
    else:
        settings = {}
    
    settings.setdefault('app_admin', True)
except Exception:
    settings = {'app_admin': True}

if settings['app_admin'] == True:
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

import threading
from app.utils.is_opened import is_opened


threads = []
imports = []

def start(file):
    global imports
    imports[file] = __import__(file, fromlist=[""])


if not is_opened():
    threads.append(threading.Thread(target=start, args=('app.server',), daemon=True))
    threads[-1].start()
    
    start('app.tray')
    
    for thread in threads:
        thread.join()
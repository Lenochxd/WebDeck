import ctypes
import sys
import json

try:
    with open('config.json', encoding= "utf-8") as f:
        settings = json.load(f)['settings']
except FileNotFoundError:
    settings = {'app-admin': True}
    
if 'app-admin' in settings and settings['app-admin'] == 'true':
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

import threading
import win32com.client
from app.utils.is_opened import is_opened


threads = []
imports = []

def start(file):
    win32com.client.pythoncom.CoInitialize() 
    global imports
    imports[file] = __import__(file, fromlist=[""])


if is_opened() == False:
    wmi = win32com.client.GetObject("winmgmts:")
    processes = wmi.InstancesOf("Win32_Process")

    threads.append(threading.Thread(target=start, args=('app.tray',), daemon=True))
    threads[-1].start()
    
    threads.append(threading.Thread(target=start, args=('app.server',), daemon=True))
    threads[-1].start()
    
    
    for thread in threads:
        thread.join()
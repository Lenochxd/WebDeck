import threading
import win32com.client
from app.functions.is_opened import is_opened


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
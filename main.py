import pystray
from pystray import MenuItem as item
from PIL import Image
import ctypes
import sys
import win32gui, win32con
import win32com.client
import time
import subprocess
import socket
import webbrowser
import json

wmi = win32com.client.GetObject("winmgmts:")
processes = wmi.InstancesOf("Win32_Process")

if_webdeck = False
wd_count = 0
for process in processes:
    if 'webdeck' in process.Properties_('Name').Value.lower().strip():
        wd_count += 1
if wd_count > 1:
    time.sleep(1)
    wmi = win32com.client.GetObject("winmgmts:")
    processes = wmi.InstancesOf("Win32_Process")

    if_webdeck = False
    wd_count = 0
    for process in processes:
        if 'webdeck' in process.Properties_('Name').Value.lower().strip():
            wd_count += 1
    if wd_count > 1:
        if_webdeck = True
    
if if_webdeck == False:

    icon = None

    #subprocess.Popen(['WD_start.exe'])
    subprocess.Popen(['WD_main.exe'])
    
    def quit_program():
        global icon
        
        wmi = win32com.client.GetObject("winmgmts:")
        processes = wmi.InstancesOf("Win32_Process")
        
        processes_to_kill = [
            "WD_main.exe",
            "WD_start.exe",
            "nircmd.exe",
            "WebDeck.exe"
        ]
        
        for process in processes:
            if process.Properties_('Name').Value in processes_to_kill:
                process_name = process.Properties_('Name').Value.lower().strip()
                print(f"Stopping process: {process_name}")
                result = process.Terminate()
                if result == 0:
                    print("Process terminated successfully.")
                else:
                    print("Failed to terminate process.")
                    
        for process_name in processes_to_kill:
            try:
                subprocess.Popen(f"taskkill /f /IM {process_name}", shell=True)
            except Exception as e:
                print(f"Failed to terminate process {process_name}: {e}")
        
        icon.stop()  # Arrêter l'icône Tray
        
        sys.exit()


    def create_tray_icon():
        global icon
        image = Image.open("static/files/icon.ico")

        # Créer le menu de l'icône Tray
        menu = (
            #item('Réouvrir', lambda: window.deiconify()),
            item('Open config', lambda: webbrowser.open(f"https://{socket.gethostbyname(socket.gethostname())}:{config['url']['port']}?config=show")),
            item('Quit', lambda: quit_program()),
        )

        # Créer l'icône Tray
        icon = pystray.Icon("name", image, "WebDeck", menu)
        return icon

    create_tray_icon()
    icon.run()
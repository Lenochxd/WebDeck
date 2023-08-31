import ctypes
import sys

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()
    exit()
    
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk
import os
import win32gui, win32con
import win32com.client
import time
import subprocess
import socket
import webbrowser
import json
import qrcode
import tkinter as tk
from tkinter import PhotoImage
from io import BytesIO
import webview

if not os.path.exists("config.json"):
    port = 5000
    black_theme = "true"
    open_browser = "true"
else:
    with open('config.json', encoding="utf-8") as f:
        config = json.load(f)
        if 'open-settings-in-browser' not in config['settings']:
            config['settings']['open-settings-in-browser'] = 'true'
            with open('config.json', 'w', encoding="utf-8") as json_file:
                json.dump(config, json_file, indent=4)
            open_browser = 'true'
        else:
            open_browser = config['settings']['open-settings-in-browser']
        port = config['url']['port']
        black_theme = config['front']['black-theme']
        del config

wmi = win32com.client.GetObject("winmgmts:")
processes = wmi.InstancesOf("Win32_Process")

if_webdeck = False
if getattr(sys, 'frozen', False):
    wd_count = 0
    for process in processes:
        if 'webdeck' in process.Properties_('Name').Value.lower().strip() or \
            'wd_' in process.Properties_('Name').Value.lower().strip():
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
            
            wmi = win32com.client.GetObject("winmgmts:")
            processes = wmi.InstancesOf("Win32_Process")

            wd_count = 0
            for process in processes:
                if 'wd_' in process.Properties_('Name').Value.lower().strip():
                    wd_count += 1
            if wd_count == 0:
                subprocess.Popen(['WD_main.exe'])
    
if if_webdeck == False:

    icon = None
    window = None

    if getattr(sys, 'frozen', False):
        #subprocess.Popen(['WD_start.exe'])
        wmi = win32com.client.GetObject("winmgmts:")
        processes = wmi.InstancesOf("Win32_Process")

        if_webdeck = False
        wd_count = 0
        for process in processes:
            if 'wd_' in process.Properties_('Name').Value.lower().strip():
                wd_count += 1
        if wd_count == 0:
            subprocess.Popen(['WD_main.exe'])
    else:
        subprocess.Popen('python main_server.py', shell=True)
        
    
    def quit_program():
        global icon, window

        wmi = win32com.client.GetObject("winmgmts:")
        processes = wmi.InstancesOf("Win32_Process")

        for process in processes:
            if process.Properties_('Name').Value.replace('.exe','').lower().strip() in ["wd_main","wd_start","nircmd","webdeck"]:
                print(f"Stopping process: {process.Properties_('Name').Value}")
                try: 
                    result = process.Terminate()
                except TypeError:
                    pass
                if result == 0:
                    print("Process terminated successfully.")
                else:
                    print("Failed to terminate process.")

        processes_to_kill = [
            "WD_main.exe",
            "WD_start.exe",
            "nircmd.exe",
            "WebDeck.exe"
        ]

        for process_name in processes_to_kill:
            try:
                subprocess.Popen(f"taskkill /f /IM {process_name}", shell=True)
                #subprocess.Popen(f'nircmd.exe close title "{process_name}"', shell=True)
            except Exception as e:
                print(f"Failed to terminate process {process_name}: {e}")

        close_window()
        icon.stop()  # Arrêter l'icône Tray

        sys.exit()
        exit()
    
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # N'importe quelle adresse et port, ici on utilise Google DNS
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        finally:
            s.close()
        return local_ip

    local_ip = get_local_ip()

    def open_config():
        if open_browser.lower() == 'true':
            webbrowser.open(f"http://{local_ip}:{port}?config=show")
        else:
            webview.create_window('WebDeck Config', url=f'http://{local_ip}:{port}?config=show', background_color='#141414')
            webview.start()
            foreground_window = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(foreground_window)
            if "webdeck" in window_title.lower():
                win32gui.ShowWindow(foreground_window, win32con.SW_MAXIMIZE)

    def close_window(event=None):
        global window
        window.destroy()
        del window
        window = None
    
    url = f"http://{local_ip}:{port}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Création de l'image du QR code sous forme de bytes
    img_stream = BytesIO()
    # if black_theme.lower() == "true":
    #     qr.make_image(fill_color="white", back_color="black").save(img_stream, format='PNG')
    # else:
    qr.make_image(fill_color="black", back_color="white").save(img_stream, format='PNG')
    img_stream.seek(0)

    # Convertir l'image en format PIL pour EasyGUI
    qr_pil_image = Image.open(img_stream)

    def show_qrcode():
        global window
        if window is None:
            window = tk.Tk()
            window.title("QR Code")
            
            image_tk = ImageTk.PhotoImage(image=qr_pil_image)
            
            label = tk.Label(window, image=image_tk)
            label.pack()
            
            text_label = tk.Label(window, text=f"http://{local_ip}:{port}/", font=("Helvetica", 13))
            text_label.pack()
            
            window.iconbitmap("static/files/icon.ico")
            window.lift()
            window.focus_force()
            
            window.bind("<Escape>", close_window)
            window.bind("<Return>", close_window)
            window.bind("<space>", close_window)
            
            window.resizable(width=False, height=False)
            
            window.protocol("WM_DELETE_WINDOW", close_window)
            window.mainloop()


    def create_tray_icon():
        global icon
        image = Image.open("static/files/icon.ico")

        menu = (
            item('QR Code', lambda: show_qrcode(), default=True),
            item('Open config', lambda: open_config()),
            item('Quit', lambda: quit_program()),
        )

        # Créer l'icône Tray
        if getattr(sys, 'frozen', False):
            icon = pystray.Icon("name", image, "WebDeck", menu)
        else:
            icon = pystray.Icon("name", image, "WebDeck DEV", menu)
        return icon

    create_tray_icon()
    icon.run()
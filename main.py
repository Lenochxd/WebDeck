import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk
import ctypes
import sys
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

if not os.path.exists("config.json"):
    port = 5000
    black_theme = "true"
else:
    with open('config.json', encoding="utf-8") as f:
        config = json.load(f)
        port = config['url']['port']
        black_theme = config['front']['black-theme']
        del config

wmi = win32com.client.GetObject("winmgmts:")
processes = wmi.InstancesOf("Win32_Process")

if_webdeck = False
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
    
if if_webdeck == False:

    icon = None
    window = None

    if getattr(sys, 'frozen', False):
        #subprocess.Popen(['WD_start.exe'])
        subprocess.Popen(['WD_main.exe'])
    else:
        subprocess.Popen('python main_server.py', shell=True)
        
    
    def quit_program():
        global icon, window
        
        wmi = win32com.client.GetObject("winmgmts:")
        processes = wmi.InstancesOf("Win32_Process")
        
        processes_to_kill = [
            "WD_main.exe",
            "WD_start.exe",
            "nircmd.exe",
            "WebDeck.exe"
        ]
        
        
        for process in processes:
            if process.Properties_('Name').Value.replace('.exe','').lower().strip() in ["wd_main","wd_start","nircmd","webdeck"]:
                print(f"Stopping process: {process.Properties_('Name').Value}")
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
        
        close_window()
        icon.stop()  # Arrêter l'icône Tray
        
        sys.exit()
        exit()
        
    def open_config():
        webbrowser.open(f"http://{socket.gethostbyname(socket.gethostname())}:{port}?config=show")

    def close_window(event=None):
        global window
        window.destroy()
        del window
        window = None
    
    url = f"http://{socket.gethostbyname(socket.gethostname())}:{port}"
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

            # Convert PIL image to PhotoImage
            image_tk = ImageTk.PhotoImage(image=qr_pil_image)

            label = tk.Label(window, image=image_tk)
            label.pack()

            window.iconbitmap("static/files/icon.ico")
            window.lift()  # Met la fenêtre au premier plan
            window.focus_force()  # Force le focus sur la fenêtre

            window.bind("<Escape>", close_window)  # Associer la touche "Echap" à la fermeture de la fenêtre
            window.bind("<Return>", close_window)  # Associer la touche "Entrée" à la fermeture de la fenêtre
            window.bind("<space>", close_window)  # Associer la touche "Espace" à la fermeture de la fenêtre

            window.resizable(width=False, height=False)

            window.protocol("WM_DELETE_WINDOW", close_window)  # Gérer la fermeture de la fenêtre via la barre de titre
            window.mainloop()


    def create_tray_icon():
        global icon
        image = Image.open("static/files/icon.ico")

        # Créer le menu de l'icône Tray
        menu = (
            #item('Réouvrir', lambda: window.deiconify()),
            item('QR Code', lambda: show_qrcode(), default=True),
            item('Open config', lambda: open_config()),
            item('Quit', lambda: quit_program()),
        )

        # Créer l'icône Tray
        icon = pystray.Icon("name", image, "WebDeck", menu)
        return icon

    create_tray_icon()
    icon.run()
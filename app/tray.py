import sys  
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk
import os
import win32gui, win32con
import win32com.client
import subprocess
import socket
import webbrowser
import json
import qrcode
import tkinter as tk
from io import BytesIO
import webview

from app.utils.firewall import fix_firewall_permission
from app.utils.get_local_ip import get_local_ip


def reload_config():
    port = 5000
    black_theme = "true"
    open_in_integrated_browser = "true"
    language = "en_US"

    if os.path.exists("config.json"):
        with open('config.json', encoding="utf-8") as f:
            config = json.load(f)
            settings = config.get('settings', {})
            integrated_browser_key = 'open-settings-in-integrated-browser'
            browser_key = 'open-settings-in-browser'
            
            if browser_key in config['settings']:
                settings[integrated_browser_key] = 'false' if open_in_integrated_browser else 'true'
                settings.pop(browser_key, None)
                
            open_in_integrated_browser = settings.get(integrated_browser_key, 'false') == 'true'
            print(open_in_integrated_browser)
            with open('config.json', 'w', encoding="utf-8") as json_file:
                json.dump(config, json_file, indent=4)

            port = config['url']['port']
            black_theme = config['front']['black-theme']
            language = config['settings']['language']

    return port, black_theme, language, open_in_integrated_browser

port, black_theme, language, open_in_integrated_browser = reload_config()

wmi = win32com.client.GetObject("winmgmts:")
processes = wmi.InstancesOf("Win32_Process")



icon = None
window = None
    
def load_lang_file(lang):
    lang_dictionary = {}
    lang_path = f"webdeck/translations/{lang}.lang"
    if not os.path.isfile(f"static/files/langs/{lang}.lang"):
        for root, dirs, files in os.walk('static/files/langs'):
            for file in files:
                if file.endswith('.lang') and file.startswith(lang):
                    lang_path = f"static/files/langs/{file}"
                    
    with open(lang_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.replace(' ', '').replace('\n','') != '' and not line.startswith('//') and not line.startswith('#'):
                try:
                    key, value = line.strip().split('=')
                    lang_dictionary[key] = value.strip()
                except:
                    print(line)
    return lang_dictionary

text = load_lang_file(language)

def exit_program():
    global icon, window

    wmi = win32com.client.GetObject("winmgmts:")
    processes = wmi.InstancesOf("Win32_Process")

    processes_to_kill = [
        "WD_main.exe",
        "WD_start.exe",
        "nircmd.exe",
        "WebDeck.exe"
    ]

    for process_name in processes_to_kill:
        try:
            subprocess.Popen(f"taskkill /f /IM {process_name}", shell=True)
        except Exception as e:
            print(f"Failed to terminate process {process_name}: {e}")

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

    if not getattr(sys, 'frozen', False):
        try:
            subprocess.Popen("taskkill /f /IM python.exe", shell=True)
        except Exception as e:
            print(f"Failed to terminate process {process_name}: {e}")

    close_window()
    icon.stop()  # Stop Tray Icon

    exit()


local_ip = get_local_ip()

def open_config():
    port, black_theme, language, open_in_integrated_browser = reload_config()
    if open_in_integrated_browser == True:
        webview.create_window('WebDeck Config', url=f'http://{local_ip}:{port}?config=show', background_color='#141414')
        webview.start()
        foreground_window = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(foreground_window)
        if "webdeck" in window_title.lower():
            win32gui.ShowWindow(foreground_window, win32con.SW_MAXIMIZE)
    else:
        webbrowser.open(f"http://{local_ip}:{port}?config=show")

def close_window(event=None):
    global window
    if window:
        window.destroy()
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

# Creation of the QR code image in bytes
img_stream = BytesIO()
# if black_theme.lower() == "true":
#     qr.make_image(fill_color="white", back_color="black").save(img_stream, format='PNG')
# else:
qr.make_image(fill_color="black", back_color="white").save(img_stream, format='PNG')
img_stream.seek(0)

# Convert image to PIL format for EasyGUI
qr_pil_image = Image.open(img_stream)

def show_qrcode():
    global window
    if window is None:
        window = tk.Tk()
        window.title(text['qr_code'])
        
        image_tk = ImageTk.PhotoImage(image=qr_pil_image)
        
        label = tk.Label(window, image=image_tk)
        label.pack()
        
        text_label = tk.Label(window, text=f"http://{local_ip}:{port}/", font=("Helvetica", 13))
        text_label.pack()
        
        window.iconbitmap("static/assets/icon.ico")
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
    image = Image.open("static/assets/icon.ico")

    menu = (
        item(text['qr_code'], lambda: show_qrcode(), default=True),
        item(text['open_config'], lambda: open_config()),
        item(text['fix_firewall'], lambda: fix_firewall_permission()),
        item(text['exit'], lambda: exit_program()),
    )

    # Create the Tray Icon
    if getattr(sys, 'frozen', False):
        icon = pystray.Icon("name", image, "WebDeck", menu)
    else:
        icon = pystray.Icon("name", image, "WebDeck DEV", menu)
    return icon

create_tray_icon()
icon.run()
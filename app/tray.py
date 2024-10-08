import sys  
import pystray
import os
import win32gui, win32con
import win32com.client
import subprocess
import webbrowser
import json
import qrcode
import webview
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

from app.utils.firewall import fix_firewall_permission
from app.utils.get_local_ip import get_local_ip
from app.utils.load_lang_file import load_lang_file

def reload_config():
    port = 59997
    dark_theme = True
    open_in_integrated_browser = True
    language = "en_US"

    config_path = None
    if os.path.exists(".config/config.json"):
        config_path = ".config/config.json"
    elif os.path.exists("config.json"):
        config_path = "config.json"
    
    if config_path:
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
            settings = config.get('settings', {})
            integrated_browser_key = 'open_settings_in_integrated_browser'
            browser_key = 'open-settings-in-browser'
            
            # update config to remove 'open-settings-in-browser'
            if browser_key in config['settings']:
                settings[integrated_browser_key] = not config['settings'].get(browser_key, False)
                settings.pop(browser_key, None)
                
            open_in_integrated_browser = settings.get(integrated_browser_key, False)
            print('open_in_integrated_browser:', open_in_integrated_browser)
            with open('.config/config.json', 'w', encoding="utf-8") as json_file:
                json.dump(config, json_file, indent=4)

            port = config['url']['port']
            dark_theme = config['front'].get('dark-theme', config['front'].get('black-theme', True))
            language = config['settings']['language']

    return port, dark_theme, language, open_in_integrated_browser

port, dark_theme, language, open_in_integrated_browser = reload_config()
text = load_lang_file(language)

icon = None
window = None


def exit_program():
    global icon, window

    if not getattr(sys, 'frozen', False):
        try:
            subprocess.Popen("taskkill /f /IM python.exe", shell=True)
        except Exception as e:
            print(f"Failed to terminate process {process_name}: {e}")
    else:
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
        

    close_window()
    icon.stop()  # Stop Tray Icon

    exit()


local_ip = get_local_ip()

def open_config():
    port, dark_theme, language, open_in_integrated_browser = reload_config()
    if open_in_integrated_browser == True:
        webview.create_window('WebDeck Config', url=f'http://{local_ip}:{port}?config=show', background_color='#141414')
        webview.start()
        foreground_window = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(foreground_window)
        if "webdeck" in window_title.lower():
            win32gui.ShowWindow(foreground_window, win32con.SW_MAXIMIZE)
    else:
        webbrowser.open(f"http://{local_ip}:{port}?config=show")

def close_window():
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
# if dark_theme == True:
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
        
        window.iconbitmap("static/icons/icon.ico")
        window.lift()
        window.focus_force()
        
        window.bind("<Escape>", close_window)
        window.bind("<Return>", close_window)
        window.bind("<space>", close_window)
        
        window.resizable(width=False, height=False)
        
        window.protocol("WM_DELETE_WINDOW", close_window)
        window.mainloop()

def generate_menu(language, server_status=1):
    print('NEW STATUS: ', server_status)
    text = load_lang_file(language)

    server_status_text = {
        0: text['server_loading'],
        1: text['server_online'],
        2: text['server_offline']
    }

    return (
        pystray.MenuItem(text['qr_code'], lambda: show_qrcode(), default=True),
        pystray.MenuItem(text['options'], pystray.Menu(
            pystray.MenuItem(text['open_config'], lambda: open_config()),
            pystray.MenuItem(text['fix_firewall'], lambda: fix_firewall_permission()),
        )),
        pystray.MenuItem(
            f"{text['server_status']} {server_status_text.get(server_status, text['server_offline'])}",
            lambda: None
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(text['report_issue'], lambda: webbrowser.open('https://github.com/Lenochxd/WebDeck/issues')),
        pystray.MenuItem(text['exit'], lambda: exit_program()),
    )

def generate_tray_icon():
    global icon
    image = Image.open("static/icons/icon.ico")

    menu = generate_menu(language, server_status=0)

    # Create the Tray Icon
    if getattr(sys, 'frozen', False):
        icon = pystray.Icon("name", image, "WebDeck", menu)
    else:
        icon = pystray.Icon("name", image, "WebDeck DEV", menu)
    return icon

def change_tray_language(new_lang):
    global icon, language
    language = new_lang
    if icon is not None:
        icon.menu = generate_menu(language)
        icon.update_menu()

def change_server_state(new_state):
    global icon
    if icon is not None:
        icon.menu = generate_menu(language, server_status=new_state)
        icon.update_menu()


def create_tray_icon():
    global icon
    if icon is None:  # Only create the icon if it doesn't already exist
        icon = generate_tray_icon()  # Replace with your actual icon creation logic
        icon.run()
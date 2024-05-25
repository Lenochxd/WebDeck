import ctypes
import sys
import os
import time
import subprocess
import socket
import webbrowser
import json
import qrcode
import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item
import win32gui
import win32con
import win32com.client
import webview


def is_user_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()


def reload_config():
    port, black_theme, language, open_in_integrated_browser = 5000, "true", "en_US", "true"

    if os.path.exists("config.json"):
        with open('config.json', encoding="utf-8") as f:
            config = json.load(f)
            settings = config.get('settings', {})
            integrated_browser_key = 'open-settings-in-integrated-browser'
            browser_key = 'open-settings-in-browser'

            if browser_key in settings:
                settings[integrated_browser_key] = 'false' if open_in_integrated_browser else 'true'
                settings.pop(browser_key, None)

            open_in_integrated_browser = settings.get(integrated_browser_key, 'false') == 'true'

            with open('config.json', 'w', encoding="utf-8") as json_file:
                json.dump(config, json_file, indent=4)

            port = config['url']['port']
            black_theme = config['front']['black-theme']
            language = settings['language']

    return port, black_theme, language, open_in_integrated_browser


def is_webdeck_running():
    wmi = win32com.client.GetObject("winmgmts:")
    processes = wmi.InstancesOf("Win32_Process")
    wd_count = sum(1 for process in processes if 'webdeck' in process.Properties_('Name').Value.lower() or 'wd_' in process.Properties_('Name').Value.lower())
    return wd_count > 1


def ensure_webdeck_running():
    if is_webdeck_running():
        time.sleep(1)
        if is_webdeck_running():
            subprocess.Popen(['WD_main.exe'])


def load_lang_file(lang):
    lang_dictionary = {}
    lang_path = f"static/files/langs/{lang}.lang"
    if not os.path.isfile(lang_path):
        for root, _, files in os.walk('static/files/langs'):
            for file in files:
                if file.endswith('.lang') and file.startswith(lang):
                    lang_path = os.path.join(root, file)

    with open(lang_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() and not line.startswith('//') and not line.startswith('#'):
                try:
                    key, value = line.strip().split('=')
                    lang_dictionary[key] = value.strip()
                except ValueError:
                    print(f"Invalid line in lang file: {line}")
    return lang_dictionary


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip


def fix_firewall_permission():
    command = [
        "powershell", "-NoProfile", "New-NetFirewallRule",
        "-DisplayName", '"WebDeck"', "-Direction", "Inbound",
        "-Program", f'"{sys.executable}"', "-Action", "Allow",
    ]
    subprocess.run(command)


def open_config(port, local_ip):
    if open_in_integrated_browser:
        webview.create_window('WebDeck Config', url=f'http://{local_ip}:{port}?config=show', background_color='#141414')
        webview.start()
        foreground_window = win32gui.GetForegroundWindow()
        if "webdeck" in win32gui.GetWindowText(foreground_window).lower():
            win32gui.ShowWindow(foreground_window, win32con.SW_MAXIMIZE)
    else:
        webbrowser.open(f"http://{local_ip}:{port}?config=show")


def exit_program():
    processes_to_kill = ["WD_main.exe", "WD_start.exe", "nircmd.exe", "WebDeck.exe"]
    wmi = win32com.client.GetObject("winmgmts:")
    processes = wmi.InstancesOf("Win32_Process")

    for process_name in processes_to_kill:
        try:
            subprocess.Popen(f"taskkill /f /IM {process_name}", shell=True)
        except Exception as e:
            print(f"Failed to terminate process {process_name}: {e}")

    for process in processes:
        if process.Properties_('Name').Value.replace('.exe', '').lower() in processes_to_kill:
            try:
                result = process.Terminate()
                if result == 0:
                    print(f"Process {process.Properties_('Name').Value} terminated successfully.")
                else:
                    print(f"Failed to terminate process {process.Properties_('Name').Value}.")
            except TypeError:
                pass

    if not getattr(sys, 'frozen', False):
        try:
            subprocess.Popen("taskkill /f /IM python.exe", shell=True)
        except Exception as e:
            print(f"Failed to terminate process python.exe: {e}")

    close_window()
    icon.stop()
    sys.exit()


def close_window(event=None):
    global window
    if window:
        window.destroy()
        window = None


def create_qrcode_image(url):
    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10, border=4
    )
    qr.add_data(url)
    qr.make(fit=True)
    img_stream = BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(img_stream, format='PNG')
    img_stream.seek(0)
    return Image.open(img_stream)


def show_qrcode(qr_pil_image, local_ip, port, text):
    global window
    if window is None:
        window = tk.Tk()
        window.title(text['qr_code'])

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


def create_tray_icon(text, qr_pil_image, local_ip, port):
    global icon
    image = Image.open("static/files/icon.ico")

    menu = (
        item(text['qr_code'], lambda: show_qrcode(qr_pil_image, local_ip, port, text), default=True),
        item(text['open_config'], lambda: open_config(port, local_ip)),
        item(text['fix_firewall'], lambda: fix_firewall_permission()),
        item(text['exit'], lambda: exit_program()),
    )

    icon_name = "WebDeck" if getattr(sys, 'frozen', False) else "WebDeck DEV"
    icon = pystray.Icon("name", image, icon_name, menu)
    icon.run()


if __name__ == "__main__":
    if not is_user_admin():
        run_as_admin()

    port, black_theme, language, open_in_integrated_browser = reload_config()

    if not is_webdeck_running():
        ensure_webdeck_running()
        subprocess.Popen(['WD_main.exe'])
    else:
        subprocess.Popen('python main_server.py', shell=True)

    local_ip = get_local_ip()
    text = load_lang_file(language)
    qr_pil_image = create_qrcode_image(f"http://{local_ip}:{port}")

    create_tray_icon(text, qr_pil_image, local_ip, port)

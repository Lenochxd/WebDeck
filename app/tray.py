import sys
import json
import win32gui, win32con
import webbrowser
import pystray
import customtkinter as ctk
import random
import qrcode
import webview
import threading
from PIL import Image, ImageTk
from io import BytesIO

from .utils.settings.get_config import get_config
from .utils.exit import exit_program
from .utils.restart import restart_program
from .utils.firewall import fix_firewall_permission
from .utils.get_local_ip import get_local_ip
from .utils.settings.get_config import get_port
from .utils.languages import text, get_languages_info, get_language, set_default_language
from .utils.logger import log


def reload_config():
    config = get_config(check_updates=True)
    settings = config.get("settings", {})
            
    return (
        config["url"]["port"],
        config["front"]["dark_theme"],
        settings["language"],
        settings["open_settings_in_integrated_browser"]
    )

window = None
icon = None
port, dark_theme, language, open_in_integrated_browser = reload_config()
local_ip = get_local_ip()

def open_config():
    port, dark_theme, language, open_in_integrated_browser = reload_config()
    config_url = f"http://{local_ip}:{get_port()}?config=show"
    
    if open_in_integrated_browser:
        webview.create_window('WebDeck Config', url=config_url, background_color='#141414')
        webview.start()
        
        foreground_window = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(foreground_window)
        
        if "webdeck" in window_title.lower():
            win32gui.ShowWindow(foreground_window, win32con.SW_MAXIMIZE)
    else:
        webbrowser.open(config_url)

def generate_qr_code(dark_theme=False):
    url = f"http://{get_local_ip()}:{get_port()}/"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img_stream = BytesIO()
    
    if dark_theme:
        qr.make_image(fill_color="white", back_color="black").save(img_stream, format='PNG')
    else:
        qr.make_image(fill_color="black", back_color="white").save(img_stream, format='PNG')
    
    img_stream.seek(0)

    return Image.open(img_stream)

def show_qrcode():
    global window, image_tk

    def close_window(event=None):
        global window
        if window:
            window.destroy()
            window = None

    def create_or_lift_window():
        global window, image_tk

        if window is not None:
            # If the window exists, just bring it to the front
            window.lift()
            window.focus_force()
        else:
            # Create the QR code window
            
            ctk.set_appearance_mode("light")  # Set the appearance mode to light
            window = ctk.CTk()
            window.title("QR Code")

            # Generate QR code and create CTkImage
            qr_pil_image = generate_qr_code()
            image_tk = ctk.CTkImage(light_image=qr_pil_image, size=(300, 300))  # Adjust size as needed

            # Add the label with the CTkImage
            label = ctk.CTkLabel(window, image=image_tk, text="")
            label.pack()

            text_label = ctk.CTkLabel(window, text=f"http://{local_ip}:{get_port()}/", font=("Helvetica", 13))
            text_label.pack()

            window.iconbitmap("static/icons/icon.ico")
            window.lift()
            window.focus_force()

            # Bind events and configure window
            window.bind("<Escape>", close_window)
            window.bind("<Return>", close_window)
            window.bind("<space>", close_window)
            window.resizable(width=False, height=False)
            window.protocol("WM_DELETE_WINDOW", close_window)

            window.mainloop()

    # Ensure GUI operations are handled in the main thread
    if threading.current_thread().name == "MainThread":
        create_or_lift_window()


def generate_menu(language, server_status=1):
    log.info(f"Server status updated: {server_status}")

    server_status_text = {
        0: text('server_loading'),
        1: text('server_online'),
        2: text('server_offline')
    }

    languages_info = get_languages_info()
    misc_languages = [lang for lang in languages_info if lang.get('misc', False)]
    non_misc_languages = [lang for lang in languages_info if not lang.get('misc', False)]

    def create_language_menu_item(lang):
        button_text = lang['code']
        if lang['native_name'] != lang['code']:
            button_text = f"{lang['native_name']} ({lang['code']})"
        return pystray.MenuItem(
            button_text,
            lambda: update_language(lang['code']),
            radio=True,
            checked=lambda item: lang['code'] == get_language(language)
        )

    language_menu_items = [create_language_menu_item(lang) for lang in non_misc_languages]

    if misc_languages:
        language_menu_items.append(pystray.Menu.SEPARATOR)
        language_menu_items.extend([create_language_menu_item(lang) for lang in misc_languages])

    return pystray.Menu(
        pystray.MenuItem(text('qr_code'), show_qrcode, default=True),
        pystray.MenuItem(text('options'), pystray.Menu(
            pystray.MenuItem(text('open_config'), open_config),
            pystray.MenuItem(text('language'), pystray.Menu(*language_menu_items)),
            pystray.MenuItem(text('restart_application'), restart_program),
            pystray.MenuItem(text('edit_port'), change_port_prompt),
            pystray.MenuItem(text('fix_firewall'), fix_firewall_permission),
        )),
        pystray.MenuItem(
            f"{text('server_status')} {server_status_text.get(server_status, text('server_offline'))}",
            open_config
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(text('report_issue'), lambda: webbrowser.open('https://github.com/Lenochxd/WebDeck/issues')),
        pystray.MenuItem(text('exit'), lambda: exit_program()),
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

def change_port_prompt():
    def save_port():
        new_port = port_entry.get()
        if validate_port_input(new_port) and new_port not in ['', str(get_port())]:
            prompt_window.destroy()  # Close the window if save is successful
            
            with open('.config/config.json', 'r') as config_file:
                config = json.load(config_file)
            config['url']['port'] = int(new_port)
            with open('.config/config.json', 'w') as config_file:
                json.dump(config, config_file, indent=4)
            
            restart_program()

    def validate_port_input(new_value):
        if new_value.isdigit():
            port = int(new_value)
            return 1 <= port <= 65535
        return new_value == ""

    def randomize_port():
        random_port = random.randint(1024, 65535)
        port_entry.delete(0, ctk.END)
        port_entry.insert(0, random_port)

    def close_prompt(event=None):
        prompt_window.destroy()

    ctk.set_appearance_mode("light")
    prompt_window = ctk.CTk()
    prompt_window.title(text('change_server_port'))
    prompt_window.geometry("300x160")
    prompt_window.resizable(False, False)
    prompt_window.iconbitmap("static/icons/icon_black.ico")

    frame = ctk.CTkFrame(prompt_window, fg_color=prompt_window.cget("fg_color"))  # Match frame color with window color
    frame.pack(expand=True, padx=10, pady=(5, 10))  # Adjust padding to bring the frame closer to the top

    ctk.CTkLabel(frame, text=text('enter_new_port')).grid(row=0, column=0, pady=(2, 2), sticky="w")  # Adjust padding
    port_entry = ctk.CTkEntry(frame, validate="key", validatecommand=(frame.register(validate_port_input), "%P"))
    port_entry.insert(0, get_port())  # Set default text field value to the current port
    port_entry.grid(row=1, column=0, pady=(2, 5), sticky="ew")  # Adjust padding

    randomize_button = ctk.CTkButton(frame, text=text("randomize"), command=randomize_port)
    randomize_button.grid(row=2, column=0, pady=5, sticky="ew")
    
    save_button = ctk.CTkButton(frame, text=text("save"), command=save_port)
    save_button.grid(row=3, column=0, pady=5, sticky="ew")

    # Key bindings
    prompt_window.bind("<Return>", lambda event: save_port())
    prompt_window.bind("<Escape>", close_prompt)

    # Focus the window and the text input
    prompt_window.lift()
    prompt_window.focus_force()
    port_entry.focus()

    prompt_window.mainloop()

def change_tray_language(new_lang):
    global icon, language
    language = new_lang
    if icon is not None:
        icon.menu = generate_menu(language)
        icon.update_menu()

def update_language(new_lang):
    set_default_language(new_lang)
    change_tray_language(new_lang)

    with open('.config/config.json', 'r') as config_file:
        config = json.load(config_file)
    
    config['settings']['language'] = new_lang
    
    with open('.config/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

def change_server_state(new_state):
    global icon
    if icon is not None:
        icon.menu = generate_menu(language, server_status=new_state)
        icon.update_menu()


def create_tray_icon():
    global icon
    if icon is None:  # Only create the icon if it doesn't already exist
        icon = generate_tray_icon()
        icon.run()
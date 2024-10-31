import os
import sys
import winreg
import subprocess
import shutil
import json
import urllib.request
import pynvml
from math import sqrt
from win32com.client import Dispatch

from app.updater import check_files, check_for_updates
from app.utils.global_variables import set_global_variable
from app.utils.plugins.load_plugins import load_plugins
from app.utils.get_local_ip import get_local_ip
from app.utils.logger import log



def check_config_update(config):
    config = check_config_hyphen_case(config)
    
    # Rename 'black_theme' to 'dark_theme'
    if "black_theme" in config["front"]:
        config["front"]["dark_theme"] = config["front"].get("black_theme", True)
        del config["front"]["black_theme"]
    
    # Make every key in settings.spotify_api lowercase
    if "spotify_api" in config["settings"]:
        config["settings"]["spotify_api"] = {k.lower(): v for k, v in config["settings"]["spotify_api"].items()}

    # Move allowed_networks to settings.allowed_networks
    if "allowed_networks" in config:
        config["settings"]["allowed_networks"].extend(config["allowed_networks"])
        del config["allowed_networks"]
    
    
    with open("webdeck/config_default.json", "r", encoding="utf-8") as f:
        default_config = json.load(f)

    def update_config_with_defaults(config, default_config):
        for section, section_value in default_config.items():
            if section not in config:
                config[section] = section_value
            elif isinstance(section_value, dict):
                for key, value in section_value.items():
                    if key not in config[section]:
                        config[section][key] = value
                    elif isinstance(value, dict) and key != "buttons":
                        if key not in config[section]:
                            config[section][key] = value
                        else:
                            update_config_with_defaults(config[section][key], value)

    update_config_with_defaults(config, default_config)

    config = check_config_themes(config)
    config = check_config_booleans(config)

    return config


def check_config_themes(config):
    # Get available theme files
    themes = [
        f"//{file_name}"
        for file_name in os.listdir(".config/themes/")
        if file_name.endswith(".css")
    ]
    if "themes" not in config["front"]:
        config["front"]["themes"] = themes
    else:
        # check if there's new themes installed
        installed_themes = config["front"]["themes"]
        new_themes = [theme for theme in themes if not any(theme.endswith(name) for name in installed_themes)]
        if new_themes:
            log.debug(f"New themes found: {new_themes}")
            config["front"]["themes"].extend(iter(new_themes))

    # Check for deleted themes
    try:
        config["front"]["themes"] = eval(config["front"]["themes"])
    except TypeError:
        pass
    for theme in config["front"]["themes"][:]:
        theme_file = theme.replace('//', '')
        if not os.path.isfile(f".config/themes/{theme_file}"):
            config["front"]["themes"].remove(theme)

    # Check for duplicates
    temporary_list = [theme.replace("//", "") for theme in config["front"]["themes"]]
    duplicates = {
        theme for theme in temporary_list if temporary_list.count(theme) > 1
    }

    # Remove duplicates
    for theme in duplicates:
        while temporary_list.count(theme) > 1:
            temporary_list.remove(theme)
            if f"//{theme}" in config["front"]["themes"]:
                config["front"]["themes"].remove(f"//{theme}")
            if theme in config["front"]["themes"]:
                config["front"]["themes"].remove(theme)

            config["front"]["themes"].insert(0, f"//{theme}")
            
    return config

def check_config_booleans(config):
    for category, settings in config.items():
        for key, value in settings.items():
            
            if isinstance(value, str):
                if value.lower() == "true":
                    config[category][key] = True
                elif value.lower() == "false":
                    config[category][key] = False
                    
            elif isinstance(value, dict):
                for setting_name, setting in value.items():
                    if isinstance(setting, str):
                        if setting.lower() == "true":
                            config[category][key][setting_name] = True
                        elif setting.lower() == "false":
                            config[category][key][setting_name] = False
    return config

def check_config_hyphen_case(config):
    def convert_to_snake_case(text):
        return text.replace('-', '_')

    new_config = {}
    for category, settings in config.items():
        new_category = convert_to_snake_case(category)
        if not isinstance(settings, dict):
            new_config[new_category] = settings
        else:
            new_config[new_category] = {}
            for key, value in settings.items():
                new_key = convert_to_snake_case(key)
                if isinstance(value, dict):
                    new_value = {convert_to_snake_case(k): v for k, v in value.items()}
                else:
                    new_value = value
                new_config[new_category][new_key] = new_value

    # Update background-color to background_color in buttons
    if 'front' in new_config and 'buttons' in new_config['front']:
        for page_name, page_content in new_config['front']['buttons'].items():
            if isinstance(page_content, list):
                for button in page_content:
                    if isinstance(button, dict) and 'background-color' in button:
                        button['background_color'] = button.pop('background-color')

    return new_config


def color_distance(color1, color2):
    """
    Calculate the distance between two colors using the Euclidean formula
    """
    r1, g1, b1 = [int(color1[i : i + 2], 16) for i in range(1, 7, 2)]
    r2, g2, b2 = [int(color2[i : i + 2], 16) for i in range(1, 7, 2)]
    return sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

def sort_colorsjson():
    try:
        with open("webdeck/colors.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        url = "https://gist.githubusercontent.com/Lenochxd/12a1927943a2ce151560e1b9585d4bfa/raw/41d5a0dc9336827cefb217c1728f0e9415b1c7b9/colors_db.json"
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
        with open("webdeck/colors.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


    # Sort colors using the distance between each pair of colors
    sorted_colors = [data[0]]  # The first color is always the same
    data.pop(0)

    while data:
        current_color = sorted_colors[-1]["hex_code"]
        nearest_color = min(
            data, key=lambda c: color_distance(current_color, c["hex_code"])
        )
        sorted_colors.append(nearest_color)
        data.remove(nearest_color)

    if not sorted_colors == data:
        with open("webdeck/colors.json", "w", encoding="utf-8") as f:
            json.dump(sorted_colors, f, indent=4)
            
def get_gpu_method():
    with open(".config/config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    if not "gpu_method" in config["settings"]:
        config["settings"]["gpu_method"] = "nvidia (pynvml)"
    if config["settings"]["gpu_method"] == "nvidia (pynvml)":
        try:
            pynvml.nvmlInit()
        except pynvml.NVMLError:
            config["settings"]["gpu_method"] = "AMD"
                
    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
        
    return config

def fix_vlc_cache():
    # https://stackoverflow.com/a/71760613/17100464
    if os.name != 'nt':
        return
    
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\VideoLAN\VLC")
        vlc_path, _ = winreg.QueryValueEx(key, "InstallDir")
        winreg.CloseKey(key)
    except FileNotFoundError:
        vlc_path = None

    if vlc_path:
        vlc_cache_gen = os.path.join(vlc_path, "vlc-cache-gen.exe")
        vlc_plugins = os.path.join(vlc_path, "plugins")
        command = f'"{vlc_cache_gen}" "{vlc_plugins}"'
        try:
            subprocess.run(command, shell=True, check=True)
        except Exception as e:
            log.exception(e, "Failed to execute VLC cache generation command")



def on_start():
    # Create config.json
    if not os.path.exists(".config"):
        os.makedirs(".config")
        
    if not os.path.exists(".config/config.json"):
        if os.path.exists("config.json"):
            shutil.move("config.json", ".config/config.json")
        else:
            shutil.copy("webdeck/config_default.json", ".config/config.json")
        
        if os.name == 'nt':
            
            # Set DLLs directory
            os.add_dll_directory(os.getcwd())
    
            # Add windows start menu shortcut
            file_path = (
                os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs\WebDeck.lnk"
            )
            if not os.path.exists(file_path) and getattr(sys, "frozen", False):
                dir = os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs"
                name = "WebDeck.lnk"
                path = os.path.join(dir, name)
                target = os.getcwd() + r"\\WebDeck.exe"
                working_dir = os.getcwd()
                icon = os.getcwd() + r"\\WebDeck.exe"

                shell = Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.WorkingDirectory = working_dir
                shortcut.IconLocation = icon
                shortcut.save()
                
    # Create user_uploads dir if needed
    if not os.path.exists(".config/user_uploads"):
        try:
            os.makedirs(".config/user_uploads")
        except FileExistsError:
            pass
        
    # Remove uploaded if needed
    if os.path.exists("static/files/uploaded"):
        # Move content of "static/files/uploaded" to ".config/user_uploads"
        if os.path.exists("static/files/uploaded"):
            for file in os.listdir("static/files/uploaded"):
                src = os.path.join("static/files/uploaded", file)
                dst = os.path.join(".config/user_uploads", file)
                shutil.move(src, dst)
            shutil.rmtree("static/files/uploaded")
    
    # Create themes dir if needed
    if not os.path.exists(".config/themes"):
        os.makedirs(".config/themes")
        
    # Create plugins dir if needed
    if not os.path.exists(".config/plugins"):
        os.makedirs(".config/plugins")
        
    # Update new files
    check_files()
    
    # Load config & get gpu method
    config = get_gpu_method()
    
    # Checks for updates
    if config["settings"].get("auto_updates", True) == True:
        check_for_updates()
    
    # Load commands
    with open("webdeck/commands.json", encoding="utf-8") as f:
        commands = json.load(f)
        commands, all_func = load_plugins(commands)
        set_global_variable("all_func", all_func)
    
    # Get local ip
    local_ip = get_local_ip()
    if config["url"]["ip"] == "local_ip":
        config["url"]["ip"] = local_ip
        
        with open(".config/config.json", "w", encoding="utf-8") as json_file:
            json.dump(config, json_file, indent=4)
            
    # Fix VLC cache error
    fix_vlc_cache()
    
    # Colors json
    sort_colorsjson()
    
    # Config updater
    config = check_config_update(config)
    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
    
    return config, commands, local_ip
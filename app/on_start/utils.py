import os
import sys
import shutil
import json
import urllib.request
import pynvml
from math import sqrt
from win32com.client import Dispatch

from app.updater import check_files, check_for_updates
from app.utils.global_variables import set_global_variable
from app.utils.load_lang_file import load_lang_file
from app.utils.plugins.load_plugins import load_plugins
from app.utils.get_local_ip import get_local_ip



def check_config_update(config):
    if "background" in config["front"]:
        if (
            type(config["front"]["background"]) == "str"
            and len(config["front"]["background"]) > 3
        ):
            config["front"]["background"] = [config["front"]["background"]]
        if type(config["front"]["background"]) == "list" and config["front"][
            "background"
        ] in [[], [""]]:
            config["front"]["background"] = ["#141414"]
    else:
        # Set default background if not present
        config["front"]["background"] = ["#141414"]

    # Set default auto-updates setting if not present
    if "auto-updates" not in config["settings"]:
        config["settings"]["auto-updates"] = True

    # Set default windows startup setting if not present
    if "windows-startup" not in config["settings"]:
        config["settings"]["windows-startup"] = False

    # Set default flask debug setting if not present
    if "flask-debug" not in config["settings"]:
        config["settings"]["flask-debug"] = True

    # Remove open settings in browser setting if present
    if "open-settings-in-browser" in config["settings"]:
        del config["settings"]["open-settings-in-browser"]
    
    # Rename 'black-theme' to 'dark-theme'
    if "black-theme" in config["front"]:
        config["front"]["dark-theme"] = config["front"].get("black-theme", True)
        del config["front"]["black-theme"]

    # Set default open settings in integrated browser setting if not present
    if "open-settings-in-integrated-browser" not in config["settings"]:
        config["settings"]["open-settings-in-integrated-browser"] = False

    # Set default portrait rotate setting if not present
    if "portrait-rotate" not in config["front"]:
        config["front"]["portrait-rotate"] = "90"

    # Set default edit buttons color setting if not present
    if "edit-buttons-color" not in config["front"]:
        config["front"]["edit-buttons-color"] = False

    # Set default buttons color setting if not present
    if "buttons-color" not in config["front"]:
        config["front"]["buttons-color"] = ""

    # Set default soundboard settings if not present
    if "soundboard" not in config["settings"]:
        config["settings"]["soundboard"] = {
            "mic_input_device": "",
            "vbcable": "cable input",
        }

    # Set default mic input device if not present
    if "mic_input_device" not in config["settings"]["soundboard"]:
        config["settings"]["soundboard"]["mic_input_device"] = ""

    # Set default vbcable if not present
    if "vbcable" not in config["settings"]["soundboard"]:
        config["settings"]["soundboard"]["vbcable"] = "cable input"

    # Set default soundboard enabled based on mic input device
    if "enabled" not in config["settings"]["soundboard"]:
        config["settings"]["soundboard"]["enabled"] = (
            config["settings"]["soundboard"]["mic_input_device"] == ""
        )

    # Set default OBS settings if not present
    if "obs" not in config["settings"]:
        config["settings"]["obs"] = {"host": "localhost", "port": 4455, "password": ""}

    # Set default automatic firewall bypass setting if not present
    if "automatic-firewall-bypass" not in config["settings"]:
        config["settings"]["automatic-firewall-bypass"] = False

    # Set default fix stop soundboard setting if not present
    if "fix-stop-soundboard" not in config["settings"]:
        config["settings"]["fix-stop-soundboard"] = False

    # Set default optimized usage display setting if not present
    if "optimized-usage-display" not in config["settings"]:
        config["settings"]["optimized-usage-display"] = False


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
            print("new themes:", new_themes)
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
    check_files("webdeck/version.json", "temp.json")
    
    # Load config & get gpu method
    config = get_gpu_method()
    
    # Load text
    text = load_lang_file(config["settings"]["language"])
    
    # Checks for updates
    if config["settings"]["auto-updates"] == True:
        check_for_updates(text)
    
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
            
    # Colors json
    sort_colorsjson()
    
    # Config updater
    config = check_config_update(config)
    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
    
    return config, text, commands, local_ip
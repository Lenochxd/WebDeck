from app.utils.platform import is_win

import os
import sys
if is_win: import winreg
import subprocess
import shutil
import json
import urllib.request
import pynvml
import threading
from math import sqrt
if is_win: from win32com.client import Dispatch

from app.updater import check_files, check_for_updates
from app.utils.settings.get_config import get_config
from app.utils.global_variables import set_global_variable
from app.utils.plugins.load_plugins import load_plugins
from app.utils.get_local_ip import get_local_ip
from app.utils.args import get_arg
from app.utils.logger import log


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
    except Exception as e:
        log.exception(e, "Failed to load colors.json")
        try:
            url = "https://gist.githubusercontent.com/Lenochxd/12a1927943a2ce151560e1b9585d4bfa/raw/41d5a0dc9336827cefb217c1728f0e9415b1c7b9/colors_db.json"
            with urllib.request.urlopen(url) as response:
                data = json.load(response)
            with open("webdeck/colors.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            log.exception(e, "Failed to load colors.json from Gist")
            return


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
    if not is_win:
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
    config = get_config(check_updates=True, save_updated_config=True)
    
    if is_win:
        if config['settings']['windows_start_menu_shortcut']:
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
        else:
            # Remove windows start menu shortcut
            
            pass  # NOTE: This section is reserved for future use. It is intended for portable versions where the start menu shortcut should be removable. 
                  # Currently, 'windows_start_menu_shortcut' is false by default, which would cause the MSI installed version to remove its start menu shortcut unintentionally.
                  # This issue will be addressed in a future update.
            
            
            # file_path = (
            #     os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs\WebDeck.lnk"
            # )
            # if os.path.exists(file_path):
            #     os.remove(file_path)
                
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
    if (config["settings"].get("auto_updates", True) or get_arg('force_update')) and not get_arg('no_auto_update'):
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
    
    # Run threaded tasks
    on_start_threaded(config)
    
    return config, commands, local_ip

def on_start_threaded(config):
    def run_threaded_tasks():
        # Fix VLC cache error
        fix_vlc_cache()
        
        # Colors json
        if config["settings"]["sort_colors_on_startup"]:
            sort_colorsjson()
    
    threading.Thread(target=run_threaded_tasks).start()
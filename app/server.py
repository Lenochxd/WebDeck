# Standard library imports
import time
import threading
import subprocess
import shutil
import re
import random
import json
import os
import sys
import importlib
import ipaddress
import inspect
import ast

# Third-party library imports
import requests
import spotipy
import spotipy.util as util
from deepdiff import DeepDiff
import mss
from PIL import Image
try: from deep_translator import GoogleTranslator
except SyntaxError: pass
import pyautogui as keyboard
import keyboard as keyboard2
import webcolors
import pyaudio
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
from flask_minify import Minify
from engineio.async_drivers import gevent # DO NOT REMOVE
import pyperclip
import win32api
import win32con
import win32gui
from win32com.client import Dispatch
from win10toast import ToastNotifier
import easygui
import psutil
import GPUtil
import pynvml

try:
    import vlc
except:
    pass
from obswebsocket import obsws, events
from obswebsocket import requests as obsrequests

# Numerical and scientific libraries
import numpy as np
import ctypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import comtypes
import math

# WebDeck imports
from app.updater import compare_versions
from app.on_start import on_start, check_json_update
from app.functions.themes.parse_themes import parse_themes
from app.functions.plugins.load_plugins import load_plugins
from app.functions.fix_firewall import fix_firewall_permission
from app.functions.load_lang_file import load_lang_file
from app.functions.audio_devices import get_audio_devices

import app.buttons.soundboard as soundboard


config, text, commands, local_ip = on_start()


def save_config(config):
    with open("config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)
    return config


def create_folders(config):
    global folders_to_create
    for folder in folders_to_create:

        config["front"]["buttons"][folder["name"]] = [
            {
                "image": "back10.svg",
                "image_size": "110%",
                "message": f"/folder {folder['parent_folder']}",
                "name": f"back to {folder['parent_folder']}",
            }
        ]

        void_count = int(config["front"]["width"]) * int(config["front"]["height"])
        for _ in range(void_count - 1):
            config["front"]["buttons"][folder["name"]].append({"VOID": "VOID"})

        print("NEW FOLDER :", folder["name"])
    folders_to_create = []
    return config


def show_error(message):
    print(message)
    ctypes.windll.user32.MessageBoxW(None, message, "WebDeck Error", 0)


def print_dict_differences(dict1, dict2):
    diff = DeepDiff(dict1, dict2, ignore_order=True)

    print("Differences found :")
    for key, value in diff.items():
        print(f"Key : {key}")
        print(f"Difference : {value}")
        print("----------------------")


def merge_dicts(d1, d2):
    """
    Merge two dictionaries taking including subdictionaries.
    Keys in d2 overwrite corresponding keys in d1, unless they are part of a subdictionary.
    """
    for key in d2:
        if key in d1 and isinstance(d1[key], dict) and isinstance(d2[key], dict):
            # Recursively, we merge the subdictionaries with the merge_dict method.
            merge_dicts(d1[key], d2[key])
        else:
            # If the key exists in d1 and it is not a subdictionary, we replace it with that of d2.
            d1[key] = d2[key]
    return d1


# resize grid ||| start

def create_matrix(config):
    matrix = []
    for folder_count, (folder_name, folder_content) in enumerate(
        config["front"]["buttons"].items()
    ):
        row_count = 0
        matrix.append([])
        for count, button in enumerate(folder_content, start=1):
            if row_count >= len(matrix[folder_count]):
                matrix[folder_count].append([])
            matrix[folder_count][row_count].append(button)
            if count % int(config["front"]["width"]) == 0:
                row_count += 1
    matrix_height = len(matrix)
    matrix_width = len(matrix[0])
    return matrix


def unmatrix(matrix):
    for folder_count, folder in enumerate(matrix):
        folderName = list(config["front"]["buttons"])[folder_count]
        config["front"]["buttons"][folderName] = []
        for row in folder:
            for button in row:
                config["front"]["buttons"][folderName].append(button)

    return config


def update_gridsize(config, new_height, new_width):
    new_height, new_width = int(new_height), int(new_width)
    matrix = create_matrix(config)
    old_height, old_width = int(config["front"]["height"]), int(
        config["front"]["width"]
    )

    # if height has changed
    if old_height != new_height:

        # if the height has increased
        if new_height > old_height:
            difference = new_height - old_height
            for count, _ in enumerate(range(difference), start=1):
                for folder_name, folder_content in config["front"]["buttons"].items():
                    for _ in range(old_width):
                        # if count % 2 == 0:
                        #     folder_content.insert(0, {"VOID": "VOID"})
                        # else:
                        folder_content.append({"VOID": "VOID"})
            matrix = create_matrix(config)

        # if the height has decreased
        if old_height > new_height:
            difference = old_height - new_height
            print("height decreased")
            for count, _ in enumerate(range(difference), start=1):
                for folder_count, folder in enumerate(matrix):
                    for row_count, row in enumerate(reversed(folder)):
                        if all(element == {"VOID": "VOID"} for element in row):
                            folder.pop(-row_count - 1)
                            break
                    else:
                        for col_count in range(len(folder[0])):
                            for row_count, row in enumerate(reversed(folder), start=1):
                                if folder[-row_count][col_count] == {"VOID": "VOID"}:
                                    num = row_count
                                    while num > 1:
                                        folder[-num][col_count] = folder[-num + 1][
                                            col_count
                                        ]
                                        num -= 1
                                    folder[-num][col_count] = {"DEL": "DEL"}
                                    break
                            else:
                                x = False
                                for colb_count in range(len(folder[0])):
                                    for rowb_count in range(len(folder)):
                                        if folder[rowb_count][colb_count] == {
                                            "VOID": "VOID"
                                        }:
                                            folder[rowb_count][colb_count] = folder[-1][
                                                col_count
                                            ]
                                            x = True
                                            break
                                    if x == True:
                                        break
                                if x == False:
                                    print("NOT ENOUGH SPACE")
                        folder.pop(-1)

    # if width has changed
    if old_width != new_width:

        # if the width has increased
        if new_width > old_width:

            difference = new_width - old_width
            new_matrix = matrix
            for count, _ in enumerate(range(difference), start=1):
                for folder_count, folder in enumerate(matrix):
                    for row_count, row in enumerate(folder):
                        # if count % 2 == 0:
                        #     new_matrix[folder_count][row_count].insert(0, {"VOID": "VOID"})
                        # else:
                        new_matrix[folder_count][row_count].append({"VOID": "VOID"})
            matrix = new_matrix

        if new_width < old_width:
            difference = old_width - new_width
            print("width decreased")
            for count, _ in enumerate(range(difference), start=1):
                for folder in matrix:
                    for col_count in range(len(folder[0])):
                        if all(
                            folder[row_count][-col_count - 1] == {"VOID": "VOID"}
                            for row_count in range(len(folder))
                        ):
                            for row_count in range(len(folder)):
                                folder[row_count].pop(-col_count - 1)
                            break
                    else:
                        element_to_del = 0
                        for row in folder:
                            element_to_del += 1
                            for element_count, element in enumerate(row):
                                if element == {"VOID": "VOID"}:
                                    row.pop(element_count)
                                    element_to_del -= 1
                                    if element_to_del == 0:
                                        break
                        if element_to_del > 0:
                            for row in folder:
                                for element_count, element in enumerate(row):
                                    if element == {"VOID": "VOID"}:
                                        row.pop(element_count)
                                        element_to_del -= 1
                                        if element_to_del == 0:
                                            break
                                if element_to_del == 0:
                                    break
                        if element_to_del > 0:
                            print("NOT ENOUGH SPACE")

    config = unmatrix(matrix)
    print(old_height, new_height)
    print(old_width, new_width)
    return config


# resize grid ||| end



# for folder_name, folder_content in config["front"]["buttons"].items():
#     for button in folder_content:
#         if 'action' not in button.keys():
#             button['action'] = {
#                 "touch_start": "click",
#                 "touch_keep": "None",
#                 "touch_end": "none",
#             }


#         if 'image' in button.keys() and not button['image'].strip() == '' and ':' in button['image'] and not button['image'].startswith('http'):
#             button['image'] = button['image'].replace('/', '\\')
#             splitted = button['image'].split('\\')
#             try:
#                 copyfile(button['image'],f'static/files/images/{splitted[-1]}')
#             except Exception:
#                 pass


for filename in os.listdir("static/files/images"):
    if " " in filename and not filename.startswith("!!"):
        new_filename = filename.replace(" ", "_")
        os.rename(
            f"static/files/images/{filename}", f"static/files/images/{new_filename}"
        )
        print(f"renamed {filename}")


if getattr(sys, "frozen", False):
    app = Flask(__name__, template_folder='../../../templates', static_folder='../../../static')
else:
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

app.jinja_env.globals.update(get_audio_devices=get_audio_devices)
if getattr(sys, "frozen", False):
    Minify(app=app, html=True, js=True, cssless=True)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

toaster = ToastNotifier()


# Set up the OBS WebSocket client
def reload_obs():
    obs_host = config["settings"]["obs"]["host"]
    obs_port = int(config["settings"]["obs"]["port"])
    obs_password = config["settings"]["obs"]["password"]

    obs = obsws(obs_host, obs_port, obs_password)

    return obs_host, obs_port, obs_password, obs


obs_host, obs_port, obs_password, obs = reload_obs()

# Set up the Spotify API client
try:
    spotify_redirect_uri = "http://localhost:8888/callback"
    spotify_scope = "user-library-modify user-library-read user-read-currently-playing user-read-playback-state user-modify-playback-state playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-follow-modify user-follow-read"
    spotify_token = util.prompt_for_user_token(
        config["settings"]["spotify-api"]["USERNAME"],
        spotify_scope,
        config["settings"]["spotify-api"]["CLIENT_ID"],
        config["settings"]["spotify-api"]["CLIENT_SECRET"],
        spotify_redirect_uri,
    )
    sp = spotipy.Spotify(auth=spotify_token)
    spotify_current_user = sp.current_user()["id"]
except:
    pass


python_threads = []
def execute_python_file(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()
    exec(file_content)

def get_current_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    return volume.GetMasterVolumeLevelScalar()


def set_volume(target_volume):
    current_volume = get_current_volume()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    while math.isclose(current_volume, target_volume, rel_tol=0.01) == False:
        if current_volume > target_volume:
            current_volume -= 0.01
        else:
            current_volume += 0.01
        volume.SetMasterVolumeLevelScalar(current_volume, None)
        time.sleep(0.01)

    return current_volume


def increase_volume(delta):
    win32api.keybd_event(win32con.VK_VOLUME_UP, 0)
    win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP)
    if delta == "":
        return get_current_volume()
    target_volume = get_current_volume() + (int(delta) / 100.0)
    return set_volume(target_volume)


def decrease_volume(delta):
    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0)
    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP)
    if delta == "":
        return get_current_volume()
    target_volume = get_current_volume() - (int(delta) / 100.0)
    return set_volume(target_volume)


def getarg(message, arg):
    return next(
        (
            x.split(f"{arg}:", 1)[1].strip()
            for x in message.split()
            if x.startswith(f"{arg}:")
        ),
        None,
    )


def find_color(hex_code, colors):
    try:
        # Finding the exact color in the JSON file
        for color in colors:
            if color["hex_code"] == hex_code:
                return color["name"]

        # If the exact color is not found, search for the closest color
        closest_color = None
        min_distance = float("inf")
        for color in colors:
            rgb1 = webcolors.hex_to_rgb(hex_code)
            rgb2 = webcolors.hex_to_rgb(color["hex_code"])
            distance = sum((a - b) ** 2 for a, b in zip(rgb1, rgb2))
            if distance < min_distance:
                min_distance = distance
                closest_color = color

        return closest_color["name"]
    except ValueError:
        return "Can not find color"


def translate(word, target_language):
    # Separate words with spaces before each capital letter
    word = "".join([f" {i}" if i.isupper() else i for i in word]).strip()
    
    if word == "Discord" or target_language.upper() == "EN":
        return word
        
    try:
        return GoogleTranslator(source="en", target=target_language).translate(word)
    except NameError:
        return word
    


def bring_window_to_front(window_title):
    # Find the window
    hwnd = win32gui.FindWindow(None, str(window_title))
    if hwnd == 0:
        print("Window not found")
        return
    # Bring the window to the foreground
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)


def get_focused_window():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        print("No window has focus")
        return None
    else:
        window_title = win32gui.GetWindowText(hwnd)
        print(f"Focused window: {window_title}")
        return window_title


def close_window(window_title):
    # Find the window
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print("Window not found")
        return
    # Close the window
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


# Find a window with a specific title
def find_window_with_name(hwnd, name):
    window_name = win32gui.GetWindowText(hwnd)
    if name.lower().replace(".exe", "") in window_name.lower().replace(".exe", ""):
        return hwnd
    return None

# Function to get the window corresponding to a given name
def get_window_by_name(name):
    hwnd = win32gui.FindWindow(None, None)
    window_hwnd = None
    while hwnd != 0:
        if find_window_with_name(hwnd, name) is not None:
            window_hwnd = hwnd
            break
        hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    return window_hwnd



def set_microphone_by_name(name):
    # TODO
    # Find the recording device with the specified name
    command = f"PowerShell -Command \"Get-WmiObject Win32_SoundDevice | Where-Object {{ $_.Name -like '*{name}*' -and $_.ConfigManagerErrorCode -eq 0 }} | Select-Object -First 1 | Invoke-CimMethod -MethodName SetDefault\""
    subprocess.run(command, shell=True)


p = pyaudio.PyAudio()
def set_speakers_by_name(speakers_name):
    device_count = p.get_device_count()

    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        if device_info["name"].lower().find(speakers_name.lower()) != -1:
            # Select the found audio device
            win32api.SendMessage(
                win32con.HWND_BROADCAST,
                win32con.WM_APPCOMMAND,
                0,
                win32api.LPARAM(0x30292),
            )
            win32api.SendMessage(
                win32con.HWND_BROADCAST,
                win32con.WM_APPCOMMAND,
                0,
                win32api.LPARAM(0x30290 + i),
            )
            break


def extract_asked_device(input_string):
    pattern = r"\['(.*?)'\]"
    matches = re.findall(pattern, input_string)
    return matches
    
def get_asked_devices():
    devices = []
    
    for folder_id, value in config["front"]["buttons"].items():
        for button in config["front"]["buttons"][folder_id]:
            if "message" in button.keys() and button["message"].startswith("/usage"):
                
                device = extract_asked_device(button["message"])
                if device is not None:
                    devices.append(device)
                    
    return devices


def get_usage(
    get_all=True if config["settings"]["optimized-usage-display"] == "false" else False,
    asked_devices=get_asked_devices()
):
    computer_info = {}
    
    # CPU
    if get_all or any(item[0] == 'cpu' for item in asked_devices):
        cpu_percent = psutil.cpu_percent()
        computer_info["cpu"] = {"usage_percent": cpu_percent}

    # Memory
    if get_all or any(item[0] == 'memory' for item in asked_devices):
        memory = psutil.virtual_memory()
        computer_info["memory"] = {}
        
        if get_all or any(item[1] == 'total_gb' for item in asked_devices):
            computer_info["memory"]["total_gb"] = round(memory.total / 1024**3, 2)
        if get_all or any(item[1] == 'used_gb' for item in asked_devices):
            computer_info["memory"]["used_gb"] = round(memory.total / 1024**3 - memory.available / 1024**3, 2)
        if get_all or any(item[1] == 'available_gb' for item in asked_devices):
            computer_info["memory"]["available_gb"] = round(memory.available / 1024**3, 2)
        if get_all or any(item[1] == 'usage_percent' for item in asked_devices):
            computer_info["memory"]["usage_percent"] = memory[2]

    # Hard disk
    if get_all or any(item[0] == 'disks' for item in asked_devices):
        computer_info["disks"] = {}
        disks = psutil.disk_partitions()
        for disk in disks:
            try:
                disk_name = disk.device.replace("\\", "").replace(":", "")
                if get_all or any(item[1] == disk_name for item in asked_devices):
                    
                    computer_info["disks"][disk_name] = {}
                    disk_usage = psutil.disk_usage(disk.device)
                    
                    if get_all or any(item[2] == "total_gb" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["total_gb"] = round(disk_usage.total / 1024**3, 2)
                    if get_all or any(item[2] == "used_gb" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["used_gb"] = round(disk_usage.used / 1024**3, 2)
                    if get_all or any(item[2] == "free_gb" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["free_gb"] = round(disk_usage.free / 1024**3, 2)
                    if get_all or any(item[2] == "usage_percent" for item in asked_devices if len(item) == 3):
                        computer_info["disks"][disk_name]["usage_percent"] = disk_usage.percent
                        
            except Exception as e:
                print("Usage Disks Error:", e)
                
    # Network
    if get_all or any(item[0] == 'network' for item in asked_devices):
        network_io_counters = psutil.net_io_counters()
        computer_info["network"] = {
            "bytes_sent": network_io_counters.bytes_sent,
            "bytes_recv": network_io_counters.bytes_recv,
        }

    # GPU
    if get_all or any(item[0] == 'gpus' for item in asked_devices):
        computer_info["gpus"] = {}
        if config["settings"]["gpu_method"] == "nvidia (pynvml)":
            try:
                num_gpus = pynvml.nvmlDeviceGetCount()
                for count in range(num_gpus):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(count)
                    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    computer_info["gpus"][f"GPU{count + 1}"] = {
                        "usage_percent": int(utilization.gpu),
                    }
            except (pynvml.nvml.NVML_ERROR_NOT_SUPPORTED, Exception):
                computer_info["gpus"]["defaultGPU"] = {}
                
                config["settings"]["gpu_method"] = "None"
                with open("config.json", "w", encoding="utf-8") as json_file:
                    json.dump(config, json_file, indent=4)
                    
        elif config["settings"]["gpu_method"] == "nvidia (GPUtil)":

            gpus = GPUtil.getGPUs()
            computer_info["gpus"] = {}
            for count, gpu in enumerate(gpus):
                computer_info["gpus"][f"GPU{count + 1}"] = {
                    "name": gpu.name,
                    "used_mb": gpu.memoryUsed,
                    "total_mb": gpu.memoryTotal,
                    "available_mb": gpu.memoryTotal - gpu.memoryUsed,
                    "usage_percent": int(gpu.load * 100),
                }
                
        else:
            computer_info["gpus"]["defaultGPU"] = {}
            
        if "GPU1" in computer_info["gpus"]:
            computer_info["gpus"]["defaultGPU"] = computer_info["gpus"]["GPU1"]
            
    if get_all == False:
        computer_info = merge_dicts(usage_example, computer_info)
    return computer_info


usage_example = get_usage(True)
print(usage_example)

@app.route("/usage", methods=["POST"])
def usage():
    return jsonify(get_usage())



# Middleware to check request IP address
@app.before_request
def check_local_network():
    remote_ip = request.remote_addr    

    netmask = '255.255.255.0'

    ip_local = ipaddress.IPv4Network(local_ip + '/' + netmask, strict=False)
    ip_remote = ipaddress.IPv4Network(remote_ip + '/' + netmask, strict=False)
    
    # print(f"local IP is: {local_ip}")
    # print(f"remote: {remote_ip}")
    # print(f"IP1: {ip_local} == IP2: {ip_remote} {ip_local == ip_remote}")
    
    # print(f'new connection established: {remote_ip}')
    
    if ip_remote != ip_local:
        # check if in allowed network list in config
        for network in config["allowed_networks"]:
            if ipaddress.IPv4Address(remote_ip) in ipaddress.IPv4Network(network):
                return
            
        return (
            "Unauthorized access: you are not on the same network as the server.",
            403,
        )


@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(message)

    return dict(mdebug=print_in_console)


# Function to get all the svgs from the theme file, so we can load them during the loading screen
def get_svgs():
    svgs = []

    with open(f"static/themes/{config['front']['theme']}", "r") as f:
        content = f.read()

        # url(...)
        matches = re.findall(r"url\(([^)]+)\)", content)

        for match in matches:
            if match.endswith(".svg"):
                svgs.append(match)

    return svgs


@app.route("/")
def home():
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

    new_config = check_json_update(config)
    with open("config.json", "w", encoding="utf-8") as json_file:
        json.dump(new_config, json_file, indent=4)
    config = new_config

    with open("commands.json", encoding="utf-8") as f:
        commands = json.load(f)
        commands = load_plugins(commands)
        
    with open("static/files/version.json", encoding="utf-8") as f:
        versions = json.load(f)
    is_exe = bool(getattr(sys, "frozen", False))

    random_bg = "//"
    while random_bg.startswith("//") == True:
        random_bg = random.choice(config["front"]["background"])
        if random_bg.startswith("**uploaded/"):
            random_bg_path = random_bg.replace("**uploaded/", "static/files/uploaded/")
            if os.path.exists(random_bg_path):
                file_name, extension = os.path.splitext(
                    os.path.basename(random_bg_path)
                )
                random_bg_90_path = f"static/files/uploaded/{file_name}-90{extension}"
                if not os.path.exists(random_bg_90_path):
                    try:
                        img = Image.open(random_bg_path)
                        img_rotated = img.rotate(-90, expand=True)
                        file_name, extension = os.path.splitext(
                            os.path.basename(random_bg_path)
                        )
                        img_rotated.save(random_bg_90_path)
                    except Exception as e:
                        print(e)
    print(f"random background: {random_bg}")

    themes = [
        file_name
        for file_name in os.listdir("static/themes/")
        if file_name.endswith(".css")
    ]
    langs = [
        file_name.replace(".lang", "")
        for file_name in os.listdir("static/files/langs/")
        if file_name.endswith(".lang")
    ]

    return render_template(
        "index.jinja",
        config=config, default_theme=config['front']['theme'], themes=themes, parsed_themes=parse_themes(text),
        commands=commands, versions=versions, random_bg=random_bg, usage_example=usage_example,
        langs=langs, text=load_lang_file(config['settings']['language']),
        svgs=get_svgs(), is_exe=is_exe, portrait_rotate=config['front']['portrait-rotate'],
        int=int, str=str, dict=dict, json=json, type=type, eval=eval, open=open,
        isfile=os.path.isfile
    )


folders_to_create = []

@app.route("/save_config", methods=["POST"])
def saveconfig():
    global config, folders_to_create, obs_host, obs_port, obs_password, obs

    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

    # Retrieve form data
    new_config = request.get_json()

    new_height = new_config["front"]["height"]
    new_width = new_config["front"]["width"]
    config = update_gridsize(config, new_height, new_width)
    config["front"]["height"] = new_height
    config["front"]["width"] = new_width

    soundboard_restart = (
        not config["settings"]["soundboard"] == new_config["settings"]["soundboard"]
    )
    obs_reload = not config["settings"]["obs"] == new_config["settings"]["obs"]

    soundboard_start = False
    soundboard_stop = False
    if (
        not config["settings"]["soundboard"]["enabled"]
        == new_config["settings"]["soundboard"]["enabled"]
    ):
        if new_config["settings"]["soundboard"]["enabled"] == "true":
            soundboard_start = True
        else:
            soundboard_stop = True

    config = check_json_update(config)
    new_config = check_json_update(new_config)

    if (
        config["settings"]["windows-startup"].lower().strip() == "false"
        and new_config["settings"]["windows-startup"].lower().strip() == "true"
    ):
        if getattr(sys, "frozen", False):
            dir = (
                os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs\Startup"
            )
            path = os.path.join(dir, "WebDeck.lnk")
            target = os.getcwd() + r"\\WebDeck.exe"
            working_dir = os.getcwd()
            icon = os.getcwd() + r"\\WebDeck.exe"

            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = working_dir
            shortcut.IconLocation = icon
            shortcut.save()
    elif (
        config["settings"]["windows-startup"].lower().strip() == "true"
        and new_config["settings"]["windows-startup"].lower().strip() == "false"
    ):
        if getattr(sys, "frozen", False):
            file_path = (
                os.getenv("APPDATA")
                + r"\Microsoft\Windows\Start Menu\Programs\Startup\WebDeck.lnk"
            )
            if os.path.exists(file_path):
                os.remove(file_path)

    config = merge_dicts(config, new_config)
    config = create_folders(config)
    config = save_config(config)

    try:
        config["front"]["background"] = config["front"]["background"].replace("['", '["').replace("']", '"]').replace("', '", "','").replace("','", '","')
        config["front"]["background"] = ast.literal_eval(config["front"]["background"])
    except TypeError:
        pass

    with open("config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)

    if soundboard_stop:
        soundboard.mic.stop()
    elif soundboard_restart or soundboard_start:
        soundboard.mic.restart()

    if obs_reload:
        obs_host, obs_port, obs_password, obs = reload_obs()

    return jsonify({"success": True})


# Save the config ENTIRELY, it does not merge anything
@app.route("/COMPLETE_save_config", methods=["POST"])
def complete_save_config():
    global folders_to_create
    # Récupère les données du formulaire
    old_height = config["front"]["height"]
    old_width = config["front"]["width"]
    config = request.get_json()
    new_height = config["front"]["height"]
    new_width = config["front"]["width"]

    config = create_folders(config)
    config = save_config(config)

    config["front"]["height"] = old_height
    config["front"]["width"] = old_width
    config = update_gridsize(config, new_height, new_width)
    config["front"]["height"] = new_height
    config["front"]["width"] = new_width
    with open("config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)

    return jsonify({"success": True})


@app.route("/save_single_button", methods=["POST"])
def save_single_button():
    data = request.get_json()
    button_folder = int(data.get("location_Folder"))
    button_index = int(data.get("location_Id"))
    button_content = data.get("content")

    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

    button_folderName = list(config["front"]["buttons"])[button_folder]
    print(
        "FETCH /save_single_button -> before :"
        + str(config["front"]["buttons"][button_folderName][button_index])
    )
    config["front"]["buttons"][button_folderName][button_index] = button_content
    print(
        "FETCH /save_single_button -> after  :"
        + str(config["front"]["buttons"][button_folderName][button_index])
    )

    with open("config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)

    return jsonify({"success": True})


# Save the config but only the buttons
@app.route("/save_buttons_only", methods=["POST"])
def save_buttons_only():
    global folders_to_create

    # Get current config first
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

    # Retrieve form data
    new_config = request.get_json()

    new_config = new_config["front"]["buttons"]

    temp_order_list = [key for key, value in config["front"]["buttons"].items()]

    sorted_buttons = {}
    for folder in temp_order_list:
        sorted_buttons[folder] = new_config.get(folder)

    config["front"]["buttons"] = sorted_buttons
    config = create_folders(config)
    config = save_config(config)
    return jsonify({"success": True})


@app.route("/get_config", methods=["GET"])
def get_config():
    global folders_to_create, config

    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

    config = create_folders(config)

    with open("config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)

    return jsonify(config)


@app.route("/upload_folderpath", methods=["POST"])
def upload_folderpath():
    path = easygui.diropenbox()
    if path is None:
        path = ""
        
    return path

@app.route("/upload_filepath", methods=["POST"])
def upload_filepath():
    filetypes = request.args.get("filetypes")
    default = '*'
    if filetypes is not None:
        filetypes = filetypes.split('_')
        filetypes = [f"*{item}" for item in filetypes]
        default = filetypes[0]

    path = easygui.fileopenbox(filetypes=filetypes, default=default)
    if path is None:
        path = ""
        
    return path


@app.route("/upload_file", methods=["POST"])
def upload_file():
    print("request:", request)
    print("request.files:", request.files)
    if "file" not in request.files:
        return jsonify({"success": False, "message": text["no_files_found_error"]})

    uploaded_file = request.files["file"]

    save_path = os.path.join("static/files/uploaded", uploaded_file.filename)
    uploaded_file.save(save_path)

    if request.form.get("info") and request.form.get("info") == "background_image":
        try:
            img = Image.open(save_path)
            img_rotated = img.rotate(-90, expand=True)
            file_name, extension = os.path.splitext(os.path.basename(save_path))
            img_rotated.save(f"static/files/uploaded/{file_name}-90{extension}")
        except Exception as e:
            print(e)

    return jsonify({"success": True, "message": text["downloaded_successfully"]})


@app.route("/create_folder", methods=["POST"])
def create_folder():
    global folders_to_create
    data = request.get_json()
    folder_name = data.get("name")
    parent_folder_name = data.get("parent_folder")

    if (
        all(item["name"] != folder_name for item in folders_to_create)
        and folder_name not in config["front"]["buttons"].keys()
    ):
        folders_to_create.append(
            {"name": f"{folder_name}", "parent_folder": f"{parent_folder_name}"}
        )
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


def kill_nircmd():
    try:
        subprocess.Popen("taskkill /f /IM nircmd.exe", shell=True)
    except:
        pass


def send_data(message=None):
    global all_func, obs, obs_host, obs_port, obs_password, obs

    command_arguments = message
    message = message.replace("<|§|>", " ")

    if message == "/bypass-windows-firewall":
        fix_firewall_permission()

    if not message.strip().replace("\n", "").replace("\r", "") == "":
        print("command recieved: " + message)
    if message.startswith("/debug-send"):
        data = {"message": "Hello, world!"}
        data = json.loads(message.replace("'", '"').replace("/debug-send", ""))
        send(data)

    elif message.startswith("/exit"):
        sys.exit("/exit received")
        
    elif message.startswith("/usage"): # this is useless btw
        asked_device = []
        
        device = extract_asked_device(message)
        if device is not None:
            asked_device.append(device)
        
        print(asked_device)
        usage = get_usage(False, asked_device)
        print(usage)
        return jsonify(usage)

    elif message.startswith("/stop_sound"):
        return soundboard.stopsound()
    elif message.startswith("/playsound "):
        message = message.replace("C:\\fakepath\\", "").replace("/playsound ", "")
        percentage = message[message.rfind(" ") + 1 :].replace(" ", "")
        try:
            sound_volume = float(percentage) / 100
            sound_file = message.replace("/playsound ", "").replace(percentage, "")
        except:
            sound_volume = float(50) / 100  # mid volume (default)
            sound_file = message.replace("/playsound ", "")

        if all(
            substring not in sound_file
            for substring in [
                ":",
                "static/files/uploaded/",
                "static\\files\\uploaded\\",
            ]
        ):
            # if it is stored directly in static/files/uploaded and not in C:\example
            sound_file = f"static/files/uploaded/{sound_file}"

        ear_soundboard = config["settings"]["ear-soundboard"].lower() == "true"
        return soundboard.playsound(sound_file, sound_volume, ear_soundboard)

    elif message.startswith("/playlocalsound "):
        message = message.replace("C:\\fakepath\\", "").replace("/playlocalsound ", "")
        percentage = message[message.rfind(" ") + 1 :].replace(" ", "")
        try:
            sound_volume = float(percentage) / 100
            sound_file = message.replace("/playlocalsound ", "").replace(percentage, "")
        except:
            sound_volume = float(50) / 100  # mid volume (default)
            sound_file = message.replace("/playlocalsound ", "")

        try:
            player = vlc.MediaPlayer(sound_file)
            player.audio_set_volume(int(sound_volume * 100))
            player.play()
            player.event_manager().event_attach(
                vlc.EventType.MediaPlayerEndReached, lambda x: soundboard.remove_player(3, player)
            )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"{exc_type} | {e} | {fname} | python line: {exc_tb.tb_lineno}")
            print("ERROR:      ", e)
            print("ERROR LINE: ", exc_tb.tb_lineno)
            show_error(f"{text['mp3_loading_error']} {sound_file}")

    elif message.startswith("/exec"):
        if "type:uploaded_file" in message:
            message = message.replace("C:\\fakepath\\", "").replace("/exec ", "").replace("type:uploaded_file", "").strip()
            if all(
                substring not in message
                for substring in [
                    ":",
                    "static/files/uploaded/",
                    "static\\files\\uploaded\\",
                ]
            ):
                # if it is stored directly in static/files/uploaded and not in C:\example
                python_file = f"static/files/uploaded/{message}"
                print(message)
                print(python_file)
                
                python_threads.append(threading.Thread(target=execute_python_file, args=(python_file,), daemon=True))
                python_threads[-1].start()
        elif "type:file_path" in message:
            python_file = message.replace("/exec ", "").replace("type:file_path", "").strip()
            
            python_threads.append(threading.Thread(target=execute_python_file, args=(python_file,), daemon=True))
            python_threads[-1].start()
        else:
            exec(message.replace("/exec", "").replace("type:single_line", "").strip())

    elif message.startswith("/batch"):
        subprocess.Popen(message.replace("/batch", "", 1).strip(), shell=True)

    elif message.startswith(("/openfolder")):
        path = message.replace("/openfolder", "", 1).replace("/opendir", "", 1).strip()
        pathtemp = path.replace('\\\\','\\').replace('\\', '/')
        
        if not ":" in pathtemp:
            path = os.path.join(os.getcwd(), path)
            if not os.path.isdir(path):
                path = os.path.join(os.path.dirname(sys.executable), path)
                if not os.path.isdir(path):
                    path = pathtemp
        else:
            path = pathtemp
            
        path = path.replace('\\\\','\\').replace('\\', '/')
        
        # if not path.endswith('/'):
        #     path += '/'
            
        if not os.path.isdir(path):
            if path.startswith('/'):
                path = path[1:]
            path = f"C:/.Code/WebDeck/{path}" # FIXME
        
        path = path.replace('/', '\\')
        print(path)
        subprocess.Popen(f'explorer "{path}"')
        # os.startfile(path)
        
    elif message.startswith(("/openfile", "/start")):
        path = message.replace("/openfile", "", 1).replace("/start", "", 1).strip()

        if "://" not in path and ":" in path:
            initial_path = os.getcwd()
            try:
                file_directory = os.path.dirname(path)
                os.chdir(file_directory)
                os.startfile(path)
            finally:
                os.chdir(initial_path)
        else:
            os.startfile(path)

    elif message.startswith("/PCshutdown"):
        subprocess.Popen("shutdown /s /f /t 0", shell=True)

    elif message.startswith("/PCrestart"):
        subprocess.Popen("shutdown /r /f /t 0", shell=True)

    elif message.startswith("/PCsleep"):
        subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)

    elif message.startswith("/PChibernate"):
        subprocess.Popen("shutdown /h /t 0", shell=True)

    elif message.startswith("/locksession"):
        subprocess.Popen("Rundll32.exe user32.dll,LockWorkStation", shell=True)

    elif message.startswith("/screensaversettings"):
        subprocess.Popen(
            "rundll32.exe desk.cpl,InstallScreenSaver toasters.scr", shell=True
        )

    elif message.startswith("/screensaver") and not message.startswith("/screensaversettings"):
        if message.endswith(("on", "/screensaver", "start")):
            subprocess.Popen("%windir%\system32\scrnsave.scr /s", shell=True)

        elif message.endswith(("hard", "full", "black")):
            subprocess.Popen("nircmd.exe monitor off", shell=True)
            kill_nircmd()

        elif message.endswith(("off", "false")):
            keyboard.press("CTRL")

    elif message.startswith("/key"):
        key = message.replace("/key", "", 1).strip()
        keyboard.press(key)

    elif message.startswith("/restartexplorer"):
        subprocess.Popen("taskkill /f /im explorer.exe", shell=True)
        time.sleep(0.5)
        subprocess.Popen("explorer.exe", shell=True)
        hwnd = get_window_by_name("explorer.exe")
        if hwnd:
            close_window(hwnd)

    elif message.startswith(("/kill", "/taskill", "/taskkill", "/forceclose")):
        window_name = (
            message.replace("/kill", "")
            .replace("/taskill", "")
            .replace("/taskkill", "")
            .replace("/forceclose", "")
        )
        hwnd = get_window_by_name(window_name)
        if hwnd:
            print(f"Window '{window_name}' found with handle : {hwnd}")
        else:
            print(f"Window '{window_name}' not found")
        try:
            close_window(hwnd)
        except:
            if not "." in window_name:
                window_name += ".exe"
            subprocess.Popen(f"taskkill /f /im {window_name}", shell=True)

    elif message.startswith("/restart"):
        exe = message.replace("/restart", "")
        if not "." in exe:
            exe += ".exe"
        subprocess.Popen(f"taskkill /f /im {exe}", shell=True)
        subprocess.Popen(f"start {exe}", shell=True)

    elif message.startswith("/clearclipboard"):
        subprocess.Popen('cmd /c "echo off | clip"', shell=True)

    elif message.startswith("/write "):
        keyboard2.write(message.replace("/write ", ""))

    elif message.startswith("/writeandsend "):
        keyboard2.write(message.replace("/writeandsend ", ""))
        keyboard2.press("ENTER")

    elif message.startswith("/volume +"):
        delta = message.replace("/volume +", "")
        if delta.strip() == "":
            increase_volume("1")
        else:
            increase_volume(delta)
    elif message.startswith("/volume -"):
        delta = message.replace("/volume -", "")
        if delta.strip() == "":
            decrease_volume(delta)
        else:
            decrease_volume("1")
    elif message.startswith("/volume set"):
        target_volume = int(message.replace("/volume set ", "")) / 100.0
        set_volume(target_volume)

    elif message.startswith(("/appvolume +", "/appvolume -", "/appvolume set")):
        comtypes.CoInitialize()
        command = message.replace("/appvolume ", "").replace("set ", "set").split()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name().lower() == command[1].lower():
                print("Current volume: %s" % volume.GetMasterVolume())
                old_volume = volume.GetMasterVolume()
                old_volume_percent = round(old_volume * 100)

                if command[0].startswith("set"):
                    target_volume = int(command[0].replace("set", ""))
                    if target_volume > 100:
                        target_volume = 100
                    if target_volume < 0:
                        target_volume = 0
                elif command[0].startswith("+"):
                    if command[0].replace("+", "") == "":
                        target_volume = old_volume_percent + 1
                    else:
                        target_volume = old_volume_percent + int(
                            command[0].replace("+", "")
                        )
                elif command[0].startswith("-"):
                    if command[0].replace("-", "") == "":
                        target_volume = old_volume_percent - 1
                    else:
                        target_volume = old_volume_percent - int(
                            command[0].replace("-", "")
                        )
                target_volume_float = target_volume / 100.0

                volume.SetMasterVolume(target_volume_float, None)
                print("New volume: %s" % volume.GetMasterVolume())

        comtypes.CoUninitialize()

    elif message.startswith("/soundcontrol mute"):
        keyboard.press("volumemute")
    elif message.startswith("/mediacontrol playpause"):
        keyboard.press("playpause")
    elif message.startswith("/mediacontrol previous"):
        keyboard.press("prevtrack")
    elif message.startswith("/mediacontrol next"):
        keyboard.press("nexttrack")

    elif message.startswith("/spotify likealbum"):
        sp = spotipy.Spotify(auth=spotify_token)
        # Get information about the user's currently playing track
        track_info = sp.current_playback()

        # If a track is currently playing, like it
        if track_info is not None:
            album_id = track_info["item"]["album"]["id"]

            is_liked = sp.current_user_saved_albums_contains(albums=[album_id])[0]
            # Add or remove like based on current state
            if is_liked:
                sp.current_user_saved_albums_delete(albums=[album_id])
                print(
                    f"Removed album {track_info['item']['album']['name']} by {track_info['item']['album']['artists'][0]['name']}"
                )
            else:
                sp.current_user_saved_albums_add(albums=[album_id])
                print(
                    f"Liked album {track_info['item']['album']['name']} by {track_info['item']['album']['artists'][0]['name']}"
                )
        else:
            print("No album currently playing.")

    elif message.startswith("/spotify playsong"):
        song_name = message.replace("/spotify playsong", "").strip()

        sp = spotipy.Spotify(auth=spotify_token)
        results = sp.search(song_name, 1, 0, "track")
        track_uri = results["tracks"]["items"][0]["uri"]
        sp.start_playback(uris=[track_uri])

    elif message.startswith("/spotify playplaylist"):
        playlist_name = message.replace("/spotify playplaylist", "").strip()

        sp = spotipy.Spotify(auth=spotify_token)
        playlists = sp.current_user_playlists() # Retrieve current user's playlists

        for playlist in playlists["items"]:
            if playlist_name.lower().strip() in playlist["name"].lower().strip():
                playlist_uri = playlist["uri"]
                sp.start_playback(context_uri=playlist_uri)
                break
        else:
            print(f"Playlist '{playlist_name}' not found.")

    elif message.startswith("/spotify likesong"):
        sp = spotipy.Spotify(auth=spotify_token)
        # Get information about the user's currently playing track
        track_info = sp.current_playback()

        # If a track is currently playing, like it
        if track_info is not None:
            track_id = track_info["item"]["id"]
            print(track_info)

            is_liked = sp.current_user_saved_tracks_contains(tracks=[track_id])[0]
            # Add or remove like based on current state
            if is_liked:
                sp.current_user_saved_tracks_delete(tracks=[track_id])
                print(
                    f"Removed track {track_info['item']['name']} by {track_info['item']['artists'][0]['name']}"
                )
            else:
                sp.current_user_saved_tracks_add(tracks=[track_id])
                print(
                    f"Liked track {track_info['item']['name']} by {track_info['item']['artists'][0]['name']}"
                )
        else:
            print("No track currently playing.")

    elif message.startswith(
        (
            "/spotify add_to_playlist",
            "/spotify remove_from_playlist",
            "/spotify add_or_remove",
        )
    ):
        playlist_name = (
            message.replace("/spotify add_to_playlist", "")
            .replace("/spotify remove_from_playlist", "")
            .replace("/spotify add_or_remove", "")
            .strip()
        )
        sp = spotipy.Spotify(auth=spotify_token)
        playlists = sp.current_user_playlists()
        playlist_id = None

        for playlist in playlists["items"]:
            if playlist["name"] == playlist_name:
                playlist_id = playlist["id"]
                break

        if playlist_id is None:
            show_error(f"Playlist named '{playlist_name}' not found.")
        else:
            playback = sp.current_playback()
            track_id = playback["item"]["id"]
            track_uri = playback["item"]["uri"]
            if "add_or_remove" in message:
                playlist_items = sp.playlist_items(
                    playlist_id, fields="items(track(uri))"
                )
                track_uris = [item["track"]["uri"] for item in playlist_items["items"]]

                if track_uri in track_uris:
                    sp.playlist_remove_all_occurrences_of_items(
                        playlist_id, [track_uri]
                    )
                    print("The track has been removed from the playlist.")
                else:
                    sp.playlist_add_items(playlist_id, [track_id])
                    print("The track has been added to the playlist.")
            elif "add_to_playlist" in message:
                sp.playlist_add_items(playlist_id, [track_id])
            elif "remove_from_playlist" in message:
                sp.playlist_remove_all_occurrences_of_items(playlist_id, [track_uri])

    elif message.startswith(
        (
            "/spotify follow_artist",
            "/spotify unfollow_artist",
            "/spotify follow_or_unfollow_artist",
        )
    ):
        # TODO: possibility to follow the specified artist
        artist = (
            message.replace("/spotify follow_artist", "")
            .replace("/spotify unfollow_artist", "")
            .replace("/spotify follow_or_unfollow_artist", "")
            .strip()
        )
        sp = spotipy.Spotify(auth=spotify_token)
        playback = sp.current_playback()
        artist_id = playback["item"]["artists"][0]["id"]
        artist_name = playback["item"]["artists"][0]["name"]
        if "follow_or_unfollow_artist" in message:
            results = sp.search(q=artist_name, type="artist")
            items = results["artists"]["items"]
            if len(items) > 0:
                artist_id = items[0]["id"]
            else:
                print(f"Unable to find artist '{artist_id}' on Spotify.")

            # Check if the user is subscribed to the corresponding artist
            response = sp.current_user_following_artists(ids=[artist_id])
            is_following = response[0]

            if is_following:
                print(f"The user is subscribed to the artist '{artist_id}'.")
                sp.user_unfollow_artists([artist_id])
                print("The artist has been removed from the subscription list.")
            else:
                print(f"The user is not subscribed to the artist '{artist_id}'.")
                sp.user_follow_artists([artist_id])
                print("The artist has been added to the subscription list.")

        elif "unfollow_artist" in message:
            sp.user_unfollow_artists([artist_id])
            print("The artist has been removed from the subscription list.")
        elif "follow_artist" in message:
            sp.user_follow_artists([artist_id])
            print("The artist has been added to the subscription list.")

    elif message.startswith(
        ("/spotify volume +", "/spotify volume -", "/spotify volume set")
    ):
        sp = spotipy.Spotify(auth=spotify_token)
        # Get the current playback information
        playback_info = sp.current_playback()

        # Check if there is an active device
        if playback_info and playback_info["is_playing"] and playback_info["device"]:
            device_id = playback_info["device"]["id"]
        else:
            print("No active devices on Spotify found.")

        # Get the current volume
        current_volume = playback_info["device"]["volume_percent"]
        print(f"Current volume: {current_volume}")

        if "-" in message:
            try:
                target_volume = current_volume - int(
                    message.replace("/spotify volume -", "")
                )
            except:
                target_volume = current_volume - 10
        elif "+" in message:
            try:
                target_volume = current_volume + int(
                    message.replace("/spotify volume +", "")
                )
            except:
                target_volume = current_volume + 10
        elif "set" in message:
            try:
                target_volume = int(message.replace("/spotify volume set", ""))
            except Exception as e:
                print(f"{text['spotify_apply_volume_error']}: {e}")
                return jsonify(
                    {
                        "success": False,
                        "message": f"{text['spotify_apply_volume_error']}: {e}",
                    }
                )
        if isinstance(target_volume, int):
            if target_volume > 100:
                target_volume = 100
            if target_volume < 0:
                target_volume = 0
            target_volume = int(target_volume)
            try:
                sp.volume(target_volume, device_id=device_id)
            except Exception as e:
                print(f"{text['spotify_volume_prenium_error']}: {e}")
                return jsonify(
                    {
                        "success": False,
                        "message": f"{text['spotify_volume_prenium_error']}: {e}",
                    }
                )

            # Get the updated volume
            playback_info = sp.current_playback()
            current_volume = playback_info["device"]["volume_percent"]
            print(f"Updated volume: {current_volume}")
        else:
            print("Volume must be an integer")

    elif message.startswith("/speechrecognition"):
        keyboard.hotkey("win", "h")

    # /colorpicker lang:en type:text|name;text-original|name-original;hex;rgb;hsl copy:text;hex;rgb;hsl copytype:raw|list showtype:raw|list remove_hex_sharp:false
    elif message.startswith("/colorpicker"):

        x, y = keyboard.position()

        # Gets the screenshot of each monitor and compares the cursor position to determine the screen
        for i, monitor in enumerate(mss.mss().monitors):
            if (
                monitor["left"] <= x < monitor["left"] + monitor["width"]
                and monitor["top"] <= y < monitor["top"] + monitor["height"]
            ):
                monitor_index = i
                break

        # Take screenshot of specific screen
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_index]
            img = sct.grab(monitor)
            screenshot = np.array(
                Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            )

        # Gets the color of the pixel under the mouse cursor
        color = screenshot[y - monitor["top"], x - monitor["left"]]

        # Convert color to HEX format
        hex_color = "#{:02x}{:02x}{:02x}".format(*color)

        # Convert color to RGB format
        rgb_color = "rgb({},{},{})".format(*color)

        # Convert color to HSL format
        r, g, b = [x / 255.0 for x in color]
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin

        if delta == 0:
            hue = 0
        elif cmax == r:
            hue = ((g - b) / delta) % 6
        elif cmax == g:
            hue = (b - r) / delta + 2
        else:
            hue = (r - g) / delta + 4

        hue = round(hue * 60)
        if hue < 0:
            hue += 360

        lightness = (cmax + cmin) / 2
        saturation = 0 if delta == 0 else delta / (1 - abs(2 * lightness - 1))

        hsl_color = "hsl({}, {:.2f}%, {:.2f}%)".format(
            hue, saturation * 100, lightness * 100
        )

        target_language = getarg(message, "lang")
        selectedtypes = getarg(message, "type")
        typestocopy = getarg(message, "copy")
        copytype = getarg(message, "copytype")
        showtype = getarg(message, "showtype")
        try:
            remove_hex_sharp = getarg(message, "remove_hex_sharp").capitalize()
        except AttributeError:
            remove_hex_sharp = None
        print("------------------------------------------")
        print(target_language)
        print(selectedtypes)
        print(typestocopy)
        print(copytype)
        print(showtype)
        print(remove_hex_sharp)
        print("------------------------------------------")

        with open("colors.json", "r", encoding="utf-8") as f:
            colorsjson = json.load(f)
        if target_language is None or target_language == "en":
            named_original = find_color(hex_color, colorsjson)
            named_color = named_original
        else:
            named_original = find_color(hex_color, colorsjson)
            named_color = translate(named_original, target_language)

        types_found = {
            "NAME": named_color,
            "TEXT": named_color,
            "NAME-ORIGINAL": named_original,
            "TEXT-ORIGINAL": named_original,
            "HEX": hex_color,
            "RGB": rgb_color,
            "HSL": hsl_color,
        }

        types_found_final = {}
        if selectedtypes:
            for type in selectedtypes.split(";"):
                for type_found, value in types_found.items():
                    if type.upper() in type_found:
                        if "HEX" in type.upper() and remove_hex_sharp == "True":
                            types_found_final[type.upper()] = value.replace("#", "")
                        else:
                            types_found_final[type.upper()] = value
            print(types_found_final)
        else:
            for type_found, value in types_found.items():
                if not any(elem in type_found for elem in ["TEXT", "ORIGINAL"]):
                    types_found_final[type_found] = value
            print(types_found_final)

        # copy:text;hex;rgb;hsl copytype:raw|list
        typestocopy_final = {}
        if typestocopy:
            for type in typestocopy.split(";"):
                for type_found, value in types_found.items():
                    if type.upper() in type_found:
                        if "HEX" in type.upper() and remove_hex_sharp == "True":
                            typestocopy_final[type.upper()] = value.replace("#", "")
                        else:
                            typestocopy_final[type.upper()] = value
            if copytype.lower() == "list":
                if len(typestocopy.split(";")) == 1:
                    pyperclip.copy(str(typestocopy_final)[:-2][2:].replace("'", ""))
                else:
                    pyperclip.copy(
                        str(typestocopy_final)
                        .replace("', ", ",\n")[:-2][2:]
                        .replace("'", "")
                    )
            else:
                if len(typestocopy.split(";")) == 1:
                    pyperclip.copy(list(typestocopy_final.values())[0])
                else:
                    pyperclip.copy(", ".join(typestocopy_final.values()))

        title = "WebDeck Color Picker"
        icon = "static\\files\\icon.ico"
        duration = 5
        message = ""
        if showtype and showtype.lower() != "list":
            if typestocopy and len(typestocopy.split(";")) == 1:
                message = list(types_found_final.values())[0]
            else:
                message = ", ".join(types_found_final.values())
        else:
            if typestocopy and len(typestocopy.split(";")) == 1:
                message = str(types_found_final)[:-2][2:].replace("'", "")
            else:
                message = (
                    str(types_found_final)
                    .replace("', ", ",\n")[:-2][2:]
                    .replace("'", "")
                )

        toaster.show_toast(
            title, message, icon_path=icon, duration=duration, threaded=True
        )

    elif message.startswith("/superAltF4"):
        hwnd = get_focused_window()
        if hwnd:
            close_window(hwnd)
            subprocess.Popen(f"taskkill /f /im {hwnd}", shell=True)
            subprocess.Popen(f"taskkill /f /im {hwnd}.exe", shell=True)

    # TODO: fix /firstplan
    elif message.startswith("/firstplan"):
        window_name = message.replace("/firstplan", "").strip()

        hwnd = get_window_by_name(window_name)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            keyboard2.press("ENTER")
            print(f"Window '{window_name}' brought to the foreground")
        else:
            print(f"Window '{window_name}' not found")

    elif message.startswith("/setmicrophone"):
        set_microphone_by_name(message.replace("/setmicrophone", "").strip())
        # PAS FINI
    elif message.startswith("/setoutputdevice"):
        set_speakers_by_name(message.replace("/setoutputdevice", "").strip())
        # PAS FINI

    elif message.startswith("/copy"):
        if message.strip() == "/copy":
            keyboard.hotkey("ctrl", "c")
        else:
            msg = message.replace("/copy ", "", 1)
            if msg.startswith("/copy"):
                msg = message.replace("/copy", "", 1)
            pyperclip.copy(msg)

    elif message.startswith("/paste"):
        if message.strip() == "/paste":
            keyboard.hotkey("ctrl", "v")
        else:
            msg = message.replace("/paste ", "", 1)
            if msg.startswith("/paste"):
                msg = message.replace("/paste", "", 1)
            pyperclip.copy(msg)
            keyboard.hotkey("ctrl", "v")

    elif message.startswith("/cut"):
        keyboard.hotkey("ctrl", "x")

    elif message.startswith("/clipboard"):
        keyboard.hotkey("win", "v")

    # OBS  -  https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md
    #         https://github.com/Elektordi/obs-websocket-py

    if message.startswith("/obs_"):
        try:
            obs = obsws(obs_host, obs_port, obs_password)
            obs.connect()
        except Exception as e:
            if "10061" in str(e):
                e = text["obs_error_10061"]
            elif "password may be inco" in str(e):
                e = text["obs_error_incorrect_password"]
            return jsonify(
                {
                    "success": False,
                    "message": f"{text['obs_failed_connection_error'].replace('.','')}: {e}",
                }
            )

        if message.startswith("/obs_scene"):
            scene_name = message.replace("/obs_scene", "").lower().strip()

            scenes = obs.call(obsrequests.GetSceneList())
            for scene in scenes.getScenes():
                if scene["sceneName"].lower().strip() == scene_name:
                    print(f"Switching to {scene['sceneName']}")
                    obs.call(
                        obsrequests.SetCurrentProgramScene(sceneName=scene["sceneName"])
                    )

        elif message.startswith("/obs_toggle_rec"):
            result = obs.call(obsrequests.ToggleRecord())
            print("Recording toggled successfully.")
            if "failed" in str(result):
                return jsonify({"success": False, "message": f"{text['failed']} :/"})

        elif message.startswith("/obs_start_rec"):
            recording_status = obs.call(obsrequests.GetRecordStatus())
            if recording_status.getOutputActive():
                print("OBS is already recording.")
                return jsonify(
                    {"success": False, "message": text["obs_already_recording"]}
                )
            else:
                obs.call(obsrequests.StartRecord())
                print("Recording started successfully.")

        elif message.startswith("/obs_stop_rec"):
            recording_status = obs.call(obsrequests.GetRecordStatus())
            if recording_status.getOutputActive():
                obs.call(obsrequests.StopRecord())
                print("Recording stopped successfully.")
            else:
                print("OBS is not recording.")
                return jsonify({"success": False, "message": text["obs_not_recording"]})

        elif message.startswith("/obs_toggle_rec_pause"):
            result = obs.call(obsrequests.ToggleRecordPause())
            print("Play/pause toggled successfully.")
            if "failed" in str(result):
                return jsonify({"success": False, "message": f"{text['failed']} :/"})

        elif message.startswith("/obs_pause_rec"):
            recording_status = obs.call(obsrequests.GetRecordStatus())
            if recording_status.getOutputActive():
                result = obs.call(obsrequests.PauseRecord())
                if "failed" in str(result):
                    return jsonify({"success": False, "message": text["obs_no_recording_can_be_paused"]})
            else:
                return jsonify({"success": False, "message": text["obs_no_recording_can_be_paused"]})

        elif message.startswith("/obs_resume_rec"):
            result = obs.call(obsrequests.ResumeRecord())
            if "failed" in str(result):
                return jsonify({"success": False, "message": text["obs_no_recording_is_paused"]})

        elif message.startswith("/obs_toggle_stream"):
            result = obs.call(obsrequests.ToggleStream())
            print("Streaming toggled successfully.")
            if "failed" in str(result):
                return jsonify({"success": False, "message": f"{text['failed']} :/"})

        elif message.startswith("/obs_start_stream"):
            recording_status = obs.call(obsrequests.GetStreamStatus())
            if recording_status.getOutputActive():
                print("OBS is already streaming.")
                return jsonify({"success": False, "message": text["obs_already_streaming"]})
            else:
                obs.call(obsrequests.StartStream())
                print("Stream started successfully.")

        elif message.startswith("/obs_stop_stream"):
            recording_status = obs.call(obsrequests.GetStreamStatus())
            if recording_status.getOutputActive():
                obs.call(obsrequests.StopStream())
                print("Stream stopped successfully.")
            else:
                print("OBS is not streaming.")
                return jsonify({"success": False, "message": text["obs_not_streaming"]})

        elif message.startswith("/obs_toggle_virtualcam"):
            result = obs.call(obsrequests.ToggleVirtualCam())
            print("Virtual cam toggled successfully.")
            if "failed" in str(result):
                return jsonify({"success": False, "message": f"{text['failed']} :/"})

        elif message.startswith("/obs_start_virtualcam"):
            recording_status = obs.call(obsrequests.GetVirtualCamStatus())
            print("obs recording_status: ", recording_status)
            if recording_status.getOutputActive():
                print("Virtual cam is already started.")
                return jsonify({"success": False, "message": text["obs_already_vcam"]})
            else:
                obs.call(obsrequests.StartVirtualCam())
                print("Virtual cam started successfully.")

        elif message.startswith("/obs_stop_virtualcam"):
            recording_status = obs.call(obsrequests.GetVirtualCamStatus())
            if recording_status.getOutputActive():
                obs.call(obsrequests.StopVirtualCam())
                print("Virtual cam stopped successfully.")
            else:
                print("Virtual cam is already stopped.")
                return jsonify({"success": False, "message": text["obs_no_vcam"]})

        elif message.startswith("/obs_key"):
            hotkey=message.split(' ')[-1]
            result = obs.call(obsrequests.TriggerHotkeyByKeySequence(keyId="OBS_KEY_"+hotkey))
            if "failed" in str(result):
                print("ERROR:      ", result)
                return jsonify({"success": False, "message": f"{text['failed']} :/"})
            print("Hotkey triggered successfully.")

        obs.disconnect()
        
    else:
        for commands in all_func.values():
            for command, func in commands.items():
                if message.replace('/', '').startswith(command):
                    params = inspect.signature(func).parameters
                    param_names = [param for param in params]
                    
                    command_arguments = command_arguments.replace(f"/{command} ", '', 1)
                    commandArgs = command_arguments.split("<|§|>")
                    
                    if param_names == []:
                        func()
                    else:
                        func(*commandArgs)
                        
    return jsonify({"success": True})


@socketio.event
def send(data):
    socketio.emit("json_data", data)


@socketio.on("connect")
def socketio_connect():
    print("Socketio client connected")
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)


@socketio.on("message_from_socket")
def send_data_socketio(message):
    return send_data(message=message)


@app.route("/send-data", methods=["POST"])
def send_data_route():
    return send_data(message=request.get_json()["message"])


def check_for_updates():
    if os.path.exists("update"):
        shutil.rmtree("update", ignore_errors=True)

    try:
        with open("static/files/version.json", encoding="utf-8") as f:
            current_version = json.load(f)["versions"][0]["version"]

        url = "https://api.github.com/repos/Lenochxd/WebDeck/releases?per_page=1"
        response = requests.get(url)
        releases = response.json()
        latest_release = next((release for release in releases if not release["draft"]), None)
        latest_version = latest_release["tag_name"].replace('v', '')

        if compare_versions(latest_version, current_version) > 0:
            print(f"New version available: {latest_version}")

            os.makedirs("update")
            shutil.copyfile("python3.dll", "update/python3.dll")
            shutil.copyfile("python311.dll", "update/python311.dll")
            shutil.copyfile("WD_updater.exe", "update/WD_updater.exe")
            shutil.copytree("lib", "update/lib")

            subprocess.Popen(["update/WD_updater.exe"])

            sys.exit()

    except Exception as e:
        show_error(f"{text['auto_update_error']} \n\n{text['error']}: {e}")


def check_for_updates_loop():
    while True:

        with open("config.json", encoding="utf-8") as f:
            config = json.load(f)
        if "auto-updates" in config["settings"].keys():
            if config["settings"]["auto-updates"].lower().strip() == "true":
                check_for_updates()
        else:
            config["settings"]["auto-updates"] = "true"
            check_for_updates()
        with open("config.json", "w", encoding="utf-8") as json_file:
            json.dump(config, json_file, indent=4)

        time.sleep(3600)


if config["settings"]["auto-updates"].lower().strip() == "true":
    check_for_updates()


def check_firewall_permission():
    try:
        firewall_manager = Dispatch("HNetCfg.FwMgr")
        policy = firewall_manager.LocalPolicy.CurrentProfile
        authorized_applications = policy.AuthorizedApplications

        for app in authorized_applications:
            if app.ProcessImageFileName.lower() == sys.executable.lower():
                print(f"The application ({sys.executable}) has permission to pass through the firewall.")
                return True

        print(f"The application ({sys.executable}) does not have permission to pass through the firewall.")
        return False
    except Exception as e:
        print(f"Error checking firewall : {e}")
        return True


if (
    config["settings"]["automatic-firewall-bypass"] == "true"
    and check_firewall_permission() == False
):
    fix_firewall_permission()

print('local_ip: ', local_ip)

app.run(
    host=local_ip,
    port=config["url"]["port"],
    debug=config["settings"]["flask-debug"] == "true",
    use_reloader=config["settings"]["flask-debug"] == "false",
)

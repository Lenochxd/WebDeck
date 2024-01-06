# Standard library imports
import time
import threading
import subprocess
import shutil
import copy
import re
import sys
import random
import json
import urllib.request
import zipfile
import os
import importlib

# Third-party library imports
import requests
import socket
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from deepdiff import DeepDiff
from uuid import UUID
import pygetwindow as gw
from pywinauto import Application
import mss
from PIL import Image
from deep_translator import GoogleTranslator
import pyautogui as keyboard
import keyboard as keyboard2
import webcolors
import pyaudio
from flask import Flask, request, jsonify, render_template, redirect, Blueprint
from flask_socketio import SocketIO, emit
from flask_minify import Minify
from engineio.async_drivers import gevent
import pyperclip
import win32api
import win32con
import win32gui
from win32com.client import Dispatch
from win10toast import ToastNotifier
import tkinter as tk
from tkinter import filedialog
import sounddevice as sd
import soundfile as sf
import psutil
import GPUtil
import pynvml
try: import vlc
except: pass
from obswebsocket import obsws, events
from obswebsocket import requests as obsrequests

# Numerical and scientific libraries
import numpy as np
import bisect
from ctypes import cast, POINTER, wintypes, WinDLL, Structure, c_char
import ctypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import comtypes
import math

os.add_dll_directory(os.getcwd())


new_user = False
if not os.path.exists("config.json"):
    shutil.copy("config_default.json", "config.json")
    new_user = True
    file_path = os.getenv('APPDATA') + r'\Microsoft\Windows\Start Menu\Programs\WebDeck.lnk'
    if not os.path.exists(file_path) and getattr(sys, 'frozen', False):
        dir = os.getenv('APPDATA') + r'\Microsoft\Windows\Start Menu\Programs'
        name = 'WebDeck.lnk'
        path = os.path.join(dir, name)
        target = os.getcwd() + r'\\WebDeck.exe'
        working_dir = os.getcwd()
        icon = os.getcwd() + r'\\WebDeck.exe'
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = working_dir
        shortcut.IconLocation = icon
        shortcut.save()
if not os.path.exists("static/files/uploaded"):
    try:
        os.makedirs("static/files/uploaded")
    except FileExistsError:
        pass
    
with open('config.json', encoding="utf-8") as f:
    config = json.load(f)

def check_json_update(config):
    if 'auto-updates' not in config['settings']:
        config['settings']['auto-updates'] = 'true'
    if 'windows-startup' not in config['settings']:
        config['settings']['windows-startup'] = 'false'
    if 'flask-debug' not in config['settings']:
        config['settings']['flask-debug'] = 'true'
    if 'open-settings-in-browser' not in config['settings']:
        config['settings']['open-settings-in-browser'] = 'true'
    if 'portrait-rotate' not in config['front']:
        config['front']['portrait-rotate'] = '90'
    if 'soundboard' not in config['settings']:
        config['settings']['soundboard'] = {
            "mic_input_device": "",
            "vbcable": "cable input"
        }
    if 'mic_input_device' not in config['settings']['soundboard']:
        config['settings']['soundboard']['mic_input_device'] = ""
    if 'vbcable' not in config['settings']['soundboard']:
        config['settings']['soundboard']['vbcable'] = "cable input"
    if 'obs' not in config['settings']:
        config['settings']['obs'] = {
            "host": "localhost",
            "port": 4455,
            "password": "secret"
        }
    return config

config = check_json_update(config)
with open('config.json', 'w', encoding="utf-8") as json_file:
    json.dump(config, json_file, indent=4)

def save_config(config):
    with open('config.json', 'w', encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
    with open('config.json', encoding="utf-8") as f:
        config = json.load(f)
    return config

def create_folders(config):
    global folders_to_create
    for folder in folders_to_create:

        config['front']['buttons'][folder['name']] = [
            {
                "image": "back10.svg",
                "image_size": "110%",
                "message": f"/folder {folder['parent_folder']}",
                "name": f"back to {folder['parent_folder']}",
            }
        ]

        void_count = int(config['front']['width']) * int(config['front']['height'])
        for _ in range(void_count-1):
            config['front']['buttons'][folder['name']].append({"VOID": "VOID"})

        print("NEW FOLDER :", folder['name'])
    folders_to_create = []
    return config

def select_audio_device(channels_type='input'):
    p = pyaudio.PyAudio()
    all_devices = []

    try:
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            
            if channels_type == 'input':
                channels = device_info['maxInputChannels']
            else:
                channels = device_info['maxOutputChannels']
            # Vérifier si le périphérique est un périphérique d'entrée actif
            if channels > 0 and device_info['hostApi'] == 0:
                ok = True
                for device in all_devices:
                    if device[device.find('(') + 1:] in device_info['name'][device_info['name'].find('(') + 1:]:
                        ok = False
                if ok and not "microsoft - input" in device_info['name'].lower():
                    print(f"Appareil {i}: {device_info['name']}")
                    all_devices.append(device_info['name'])
        del ok
        print(f"ALL: {len(all_devices)}")
        print(p.get_default_output_device_info())
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
    finally:
        p.terminate()
    return all_devices


def get_device(vbcable_device):
    # https://stackoverflow.com/questions/73884593/how-to-change-vlc-python-output-device
    try:
        player = vlc.MediaPlayer()
        mods = player.audio_output_device_enum()
        if mods:
            mod = mods
            while mod:
                mod = mod.contents
                # If VB-Cable is found, return it's module and device id
                if vbcable_device.lower() in str(mod.description).lower():
                    device = mod.device
                    return device
                mod = mod.next
    except:
        return 'ERROR_NO_VLC'
            
cable_input_device = get_device(config['settings']['soundboard']['vbcable'])
vlc_installed = cable_input_device != 'ERROR_NO_VLC'

player_vbcable = {}
player_ear_soundboard = {}
def playsound(file_path: str, sound_volume, ear_soundboard=True):
    global cable_input_device, player
    if not vlc_installed:
        print("VLC is not installed!")
        return jsonify({'success': False, 'message': 'VLC is not installed!'})
    else:
        print(f"Play: {file_path}  -  volume:{sound_volume}\r\n")
        print(len(player_vbcable))
        print(player_vbcable)
        
        p_id = len(player_vbcable.keys())
        if p_id <= 3:
            player_vbcable[p_id] = vlc.MediaPlayer(file_path)
            player_vbcable[p_id].audio_set_volume(int(sound_volume * 100))
            player_vbcable[p_id].audio_output_device_set(None, cable_input_device)
            player_vbcable[p_id].play()
            player_vbcable[p_id].event_manager().event_attach(
                vlc.EventType.MediaPlayerEndReached, lambda x: remove_player(1, p_id)
            )

            if ear_soundboard:
                player_ear_soundboard[p_id] = vlc.MediaPlayer(file_path)
                player_ear_soundboard[p_id].audio_set_volume(int(sound_volume * 100))
                player_ear_soundboard[p_id].play()
                player_ear_soundboard[p_id].event_manager().event_attach(
                    vlc.EventType.MediaPlayerEndReached, lambda x: remove_player(2, p_id)
                )
                
        else:
            player_vbcable[0].stop()
            player_vbcable[0].set_time(0)
            player_vbcable[0].play()
            player_vbcable[0].event_manager().event_attach(
                vlc.EventType.MediaPlayerEndReached, lambda x: remove_player(1, p_id)
            )

            if ear_soundboard:
                player_ear_soundboard[0].stop()
                player_ear_soundboard[0].set_time(0)
                player_ear_soundboard[0].play()
                player_ear_soundboard[0].event_manager().event_attach(
                    vlc.EventType.MediaPlayerEndReached, lambda x: remove_player(2, p_id)
                )
        return jsonify({'success': True})
def remove_player(sb_type, p_id):
    global player_vbcable, player_ear_soundboard
    try:
        if sb_type == 1:
            del player_vbcable[p_id]
        elif sb_type == 2:
            del player_ear_soundboard[p_id]
        else:
            del p_id
    except KeyError:
        pass
    
def stop_soundboard():
    if not vlc_installed:
        print("VLC is not installed!")
        return jsonify({'success': False, 'message': 'VLC is not installed!'})
    else:
        global player_vbcable, player_ear_soundboard
        while True:
            try:
                for p_id, player in player_vbcable.items():
                    player.stop()
                    del player_vbcable[p_id]
                    
                for p_id, player in player_ear_soundboard.items():
                    player.stop()
                    del player_ear_soundboard[p_id]
                break
            except RuntimeError:
                ...
        return jsonify({'success': True})

def should_i_close():
    global sb_on
    if getattr(sys, 'frozen', False):
        is_handler_opened = any(
            process.info['name'].lower().strip().replace('.exe', '')
            == 'webdeck'
            for process in psutil.process_iter(['pid', 'name'])
        )
        if not is_handler_opened:
            sb_on = False
            obs.disconnect()
            sys.exit()
            exit()

def print2(message):
    print(message)
    ctypes.windll.user32.MessageBoxW(None, message, u"WebDeck Error", 0)

    
# resize grid ||| start

def create_matrix(config):
    matrix = []
    for folder_count, (folder_name, folder_content) in enumerate(config["front"]["buttons"].items()):
        row_count = 0
        matrix.append([])
        for count, button in enumerate(folder_content, start=1):
            if row_count >= len(matrix[folder_count]):
                matrix[folder_count].append([])
            matrix[folder_count][row_count].append(button)
            if count % int(config['front']['width']) == 0:
                row_count += 1
    matrix_height = len(matrix)
    matrix_width = len(matrix[0])
    return matrix

def unmatrix(matrix):
    
    for folder_count, folder in enumerate(matrix):
        folderName = list(config['front']['buttons'])[folder_count]
        config["front"]["buttons"][folderName] = []
        for row in folder:
            for button in row:
                config["front"]["buttons"][folderName].append(button)
            
    return config

def update_gridsize(config, new_height, new_width):
    new_height, new_width = int(new_height), int(new_width)
    matrix = create_matrix(config)
    old_height, old_width = int(config['front']['height']), int(config['front']['width'])

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
            print('height decreased')
            for count, _ in enumerate(range(difference), start=1):
                for folder_count, folder in enumerate(matrix):
                    for row_count, row in enumerate(reversed(folder)):
                        if all(element == {"VOID": "VOID"} for element in row):
                            folder.pop(-row_count-1)
                            break
                    else:
                        for col_count in range(len(folder[0])):
                            for row_count, row in enumerate(reversed(folder), start=1):
                                if folder[-row_count][col_count] == {"VOID": "VOID"}:
                                    num = row_count
                                    while num > 1:
                                        folder[-num][col_count] = folder[-num+1][col_count]
                                        num -= 1
                                    folder[-num][col_count] = {"DEL": "DEL"}
                                    break
                            else:
                                x = False
                                for colb_count in range(len(folder[0])):
                                    for rowb_count in range(len(folder)):
                                        if folder[rowb_count][colb_count] == {"VOID": "VOID"}:
                                            folder[rowb_count][colb_count] = folder[-1][col_count]
                                            x = True
                                            break
                                    if x == True:
                                        break
                                if x == False:
                                    print("PAS ASSEZ DE PLACE")
                        folder.pop(-1)



        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # we need to be able to remove à row even if theres no row full of voids.
        # and I DON'T KNOW how to do that I need help


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
            print('width decreased')
            for count, _ in enumerate(range(difference), start=1):
                for folder in matrix:
                    for col_count in range(len(folder[0])):
                        if all(folder[row_count][-col_count-1] == {"VOID": "VOID"} for row_count in range(len(folder))):
                            for row_count in range(len(folder)):
                                folder[row_count].pop(-col_count-1)
                            break
                    else:
                        element_to_del = 0
                        for row in folder:
                            element_to_del += 1
                            for element_count, element in enumerate(row):
                                if element == {"VOID": "VOID"}:
                                    row.pop(element_count)
                                    element_to_del -= 1
                                    if element_to_del==0: break
                        if element_to_del>0:
                            for row in folder:
                                for element_count, element in enumerate(row):
                                    if element == {"VOID": "VOID"} :
                                        row.pop(element_count)
                                        element_to_del -= 1
                                        if element_to_del==0: break
                                if element_to_del==0: break
                        if element_to_del>0:
                            print("PAS ASSEZ DE PLACE")



    config = unmatrix(matrix)
    print(old_height, new_height)
    print(old_width, new_width)
    return config


# resize grid ||| end
        

if config["front"]["background"]: 
    if type(config["front"]["background"]) == 'str':
        config["front"]["background"] = ["#141414"]
    if type(config["front"]["background"]) == 'list' and config["front"]["background"] == ['']:
        config["front"]["background"] = ["#141414"]
        
    # try:
    #     copyfile(config["front"]["background"].replace('/','\\\\'), "static/files/background-image")
    # except:
    #     pass

def getarg(message, arg):
    return next((x.split(f'{arg}:', 1)[1].strip() for x in message.split() if x.startswith(f'{arg}:')), None)

def swapPositions(list, pos1, pos2):
    try:
        list[pos1], list[pos2] = list[pos2], list[pos1]
    except Exception:
        print(f"error swapping {pos1} with {pos2}")
    return list

letters = 'abcdefghijklmnopqrstuvwxyz'
def convert_position(size, position):
    position = (letters.index(position[0])*int(size.split('x')[0])) + int(position[1]) - 1
    return position


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

    # x = int(config["front"]["width"])
    # while 'VOID' in folder_content[-1].keys():
    #     folder_content.pop(-1)

with open('config.json', 'w', encoding="utf-8") as json_file:
    json.dump(config, json_file, indent=4)


def color_distance(color1, color2):
    """
    Calcule la distance entre deux couleurs en utilisant la formule Euclidienne
    """
    r1, g1, b1 = [int(color1[i:i+2], 16) for i in range(1, 7, 2)]
    r2, g2, b2 = [int(color2[i:i+2], 16) for i in range(1, 7, 2)]
    return math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)


# Ouvrir le fichier colors.json
with open('colors.json', 'r', encoding="utf-8") as f:
    try:
        data = json.load(f)
    except Exception:
        shutil.copyfile("static/files/colorsbcp.json", "colors.json")
        with open('colors.json', 'r', encoding="utf-8") as f:
            data = json.load(f)

# Trier les couleurs en utilisant la distance entre chaque paire de couleurs
sorted_colors = [data[0]]  # La première couleur est toujours la même
data.pop(0)

while data:
    current_color = sorted_colors[-1]['hex_code']
    nearest_color = min(data, key=lambda c: color_distance(
        current_color, c['hex_code']))
    sorted_colors.append(nearest_color)
    data.remove(nearest_color)

# Enregistrer les couleurs triées dans un nouveau fichier colors2.json
with open('colors.json', 'w', encoding="utf-8") as f:
    json.dump(sorted_colors, f, indent=4)


if not os.path.isfile("nircmd.exe"):
    url = "https://www.nirsoft.net/utils/nircmd.zip"
    urllib.request.urlretrieve(url, "nircmd.zip")

    with zipfile.ZipFile("nircmd.zip", "r") as zip_ref:
        zip_ref.extractall("")

    os.remove("nircmd.zip")
    os.remove("NirCmd.chm")
    os.remove("nircmdc.exe")


for filename in os.listdir("static/files/images"):
    if ' ' in filename and not filename.startswith("!!"):
        new_filename = filename.replace(" ", "_")
        os.rename(f"static/files/images/{filename}", f"static/files/images/{new_filename}")
        print(f"renamed {filename}")


app = Flask(__name__)
app.jinja_env.globals.update(select_audio_device=select_audio_device)
if getattr(sys, 'frozen', False):
    Minify(app=app, html=True, js=True, cssless=True)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

toaster = ToastNotifier()

# Set up the OBS WebSocket client
obs_host = config['settings']['obs']['host']
obs_port = config['settings']['obs']['port']
obs_password = config['settings']['obs']['password']

obs = obsws(obs_host, obs_port, obs_password)


# Set up the Spotify API client
try:
    spotify_redirect_uri = 'http://localhost:8888/callback'
    spotify_scope = 'user-library-modify user-library-read user-read-currently-playing user-read-playback-state user-modify-playback-state playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-follow-modify user-follow-read'
    spotify_token = util.prompt_for_user_token(config['settings']['spotify-api']['USERNAME'], spotify_scope, config['settings']['spotify-api']['CLIENT_ID'], config['settings']['spotify-api']['CLIENT_SECRET'], spotify_redirect_uri)
    sp = spotipy.Spotify(auth=spotify_token)
    spotify_current_user = sp.current_user()['id']
except:
    pass


def get_current_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume.GetMasterVolumeLevelScalar()


def set_volume(target_volume):
    current_volume = get_current_volume()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
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
    if delta == '':
        return get_current_volume()
    target_volume = get_current_volume() + (int(delta) / 100.0)
    return set_volume(target_volume)

def decrease_volume(delta):
    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0)
    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP)
    if delta == '':
        return get_current_volume()
    target_volume = get_current_volume() - (int(delta) / 100.0)
    return set_volume(target_volume)


def find_color(hex_code, colors):
    try:
        # Recherche de la couleur exacte dans le fichier JSON
        for color in colors:
            if color['hex_code'] == hex_code:
                return color['name']

        # Si la couleur exacte n'est pas trouvée, recherche de la couleur la plus proche
        closest_color = None
        min_distance = float('inf')
        for color in colors:
            distance = get_color_distance(hex_code, color['hex_code'])
            if distance < min_distance:
                min_distance = distance
                closest_color = color

        return closest_color['name']
    except ValueError:
        return "Can not find color"


def get_color_distance(hex_code1, hex_code2):
    rgb1 = webcolors.hex_to_rgb(hex_code1)
    rgb2 = webcolors.hex_to_rgb(hex_code2)
    return sum((a - b) ** 2 for a, b in zip(rgb1, rgb2))


def translate(word, target_language):
    # Séparer les mots par des espaces avant chaque majuscule
    word = ''.join([f' {i}' if i.isupper() else i for i in word]).strip()
    if word == "Discord" or target_language.upper() == "EN":
        result = word
    else:
        result = GoogleTranslator(source='en', target=target_language).translate(word)

    return result

def bring_window_to_front(window_title):
    # Trouver la fenêtre
    hwnd = win32gui.FindWindow(None, str(window_title))
    if hwnd == 0:
        print("Fenêtre non trouvée")
        return
    # Mettre la fenêtre au premier plan
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)

def get_focused_window():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        print("Aucune fenêtre n'a le focus")
        return None
    else:
        window_title = win32gui.GetWindowText(hwnd)
        print(f"Fenêtre focus : {window_title}")
        return window_title

def close_window(window_title):
    # Trouver la fenêtre
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print("Fenêtre non trouvée")
        return
    # Fermer la fenêtre
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

# Fonction pour trouver une fenêtre avec un titre spécifique
def find_window_with_name(hwnd, name):
    window_name = win32gui.GetWindowText(hwnd)
    if name.lower().replace('.exe','') in window_name.lower().replace('.exe',''):
        return hwnd
    return None

# Fonction pour obtenir la fenêtre correspondant à un nom donné
def get_window_by_name(name):
    hwnd = win32gui.FindWindow(None, None)
    window_hwnd = None
    while hwnd != 0:
        if find_window_with_name(hwnd, name) is not None:
            window_hwnd = hwnd
            break
        hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    return window_hwnd

p = pyaudio.PyAudio()
def set_microphone_by_name(name):
    # Rechercher le périphérique d'enregistrement avec le nom spécifié
    command = f"PowerShell -Command \"Get-WmiObject Win32_SoundDevice | Where-Object {{ $_.Name -like '*{name}*' -and $_.ConfigManagerErrorCode -eq 0 }} | Select-Object -First 1 | Invoke-CimMethod -MethodName SetDefault\""
    subprocess.run(command, shell=True)

def set_speakers_by_name(speakers_name):
    device_count = p.get_device_count()

    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        if device_info["name"].lower().find(speakers_name.lower()) != -1:
            # Sélectionne le périphérique audio trouvé
            win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_APPCOMMAND, 0, win32api.LPARAM(0x30292))
            win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_APPCOMMAND, 0, win32api.LPARAM(0x30290 + i))
            break



# try: os.remove("static/style.css")
# except OSError: pass
# try:
#    shutil.copyfile(f"themes/{config['front']['theme']}", "static/style.css")
# except:
#    shutil.copy(f"themes/{config['front']['theme']}", "static/style.css")


# p = subprocess.Popen([sys.executable, 'mic2.py'],
#                    stdout=subprocess.PIPE,
#                    stderr=subprocess.STDOUT)

# p2 = subprocess.Popen([sys.executable, 'playsound.py'],
#                      stdin=subprocess.PIPE,
#                      stdout=subprocess.PIPE,
#                      stderr=subprocess.STDOUT)
# stdout_data, stderr_data = p2.communicate(input=bytes(f"aaaaaaaaaaaaaaa", 'utf-8'))

def has_at_least_5_minutes_difference(timestamp1, timestamp2):
    difference = abs(timestamp1 - timestamp2)
    difference_in_minutes = difference / 60
    return difference_in_minutes >= 15

with open('config.json', encoding="utf-8") as f:
    config = json.load(f)
    if not 'gpu_method' in config['settings']:
        config['settings']['gpu_method'] = 'nvidia (pynvml)'
    if config['settings']['gpu_method'] == 'nvidia (pynvml)':
        try:
            pynvml.nvmlInit()
        except pynvml.NVMLError:
            config['settings']['gpu_method'] = 'AMD'
with open('config.json', 'w', encoding="utf-8") as json_file:
    json.dump(config, json_file, indent=4)
        
excluded_disks = {}
def get_usage():
    global excluded_disks
    # CPU
    cpu_percent = psutil.cpu_percent(4)
    computer_info = {'cpu': {'usage_percent': cpu_percent}}

    # Mémoire
    memory = psutil.virtual_memory()
    computer_info['memory'] = {
        'total_gb': round(memory.total / 1024**3, 2),
        'used_gb': round(memory.total / 1024**3 - memory.available / 1024**3, 2),
        'available_gb': round(memory.available / 1024**3, 2),
        'usage_percent': memory[2]
    }

    # Disque dur
    disks = psutil.disk_partitions()
    computer_info['disks'] = {}
    for disk in disks:
        try:
            disk_name = disk.device.replace("\\", "").replace(":", "")

            # Check if the disk is excluded due to a previous error
            if disk_name not in excluded_disks.keys():

                disk_usage = psutil.disk_usage(disk.device)
                computer_info['disks'][disk_name] = {
                    'total_gb': round(disk_usage.total / 1024**3, 2),
                    'used_gb': round(disk_usage.used / 1024**3, 2),
                    'free_gb': round(disk_usage.free / 1024**3, 2),
                    'usage_percent': disk_usage.percent
                }
            elif has_at_least_5_minutes_difference(excluded_disks[disk_name.upper()], time.time()):
                del excluded_disks[disk_name.upper()]
                
        except Exception as e:
            error_message = str(e)
            print('error:', e)

            if "[WinError 5]" in error_message or "[WinError 21]" in error_message or "[WinError 1005]" in error_message:
                # Extract the disk letter following the error message
                disk_letter = error_message[-2]
                excluded_disks[disk_letter.upper()] = time.time()
                print(f"Disk '{disk_letter}' excluded from further processing for 15 minutes.")
    
    # Réseau
    network_io_counters = psutil.net_io_counters()
    computer_info['network'] = {
        'bytes_sent': network_io_counters.bytes_sent,
        'bytes_recv': network_io_counters.bytes_recv
    }

    # Carte graphique
    computer_info['gpus'] = {}
    if config['settings']['gpu_method'] == 'nvidia (pynvml)':
        num_gpus = pynvml.nvmlDeviceGetCount()
        for count in range(num_gpus):
            handle = pynvml.nvmlDeviceGetHandleByIndex(count)
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            computer_info['gpus'][f'GPU{count + 1}'] = {
                'usage_percent': int(utilization.gpu),
            }
    elif config['settings']['gpu_method'] == 'nvidia (GPUtil)':
        
        gpus = GPUtil.getGPUs()
        computer_info['gpus'] = {}
        for count, gpu in enumerate(gpus):
            computer_info['gpus'][f'GPU{count + 1}'] = {
                'name': gpu.name,
                'used_mb': gpu.memoryUsed,
                'total_mb': gpu.memoryTotal,
                'available_mb': gpu.memoryTotal - gpu.memoryUsed,
                'usage_percent': int(gpu.load * 100),
            }
    else:
        computer_info['gpus']['defaultGPU'] = {}
        
    return computer_info

usage_example = get_usage()
print(usage_example)
@app.route('/usage', methods=['POST'])
def usage():
    global usage_example
    usage_example = get_usage()
    return jsonify(usage_example)

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
if config['url']['ip'] == 'local_ip':
    config['url']['ip'] = local_ip

# Middleware pour vérifier l'adresse IP de la demande
@app.before_request
def check_local_network():
    remote_ip = request.remote_addr
    # print(f'new connection established: {remote_ip}')
    if remote_ip != local_ip and not remote_ip.startswith("127.") and not remote_ip.startswith("192.168."):
        return "Unauthorized access: you are not on the same network as the server.", 403


@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(message)

    return dict(mdebug=print_in_console)

dict_func = {}
all_func = {}
@app.route("/")
def home():
    global all_func

    should_i_close()

    with open('config.json', encoding="utf-8") as f:
        config = json.load(f)
    with open('commands.json', encoding="utf-8") as f:
        commands = json.load(f)
    with open('static/files/version.json', encoding="utf-8") as f:
        versions = json.load(f)
    is_exe = bool(getattr(sys, 'frozen', False))
    
    
    folder_path = "./addons"

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.relpath(module_path, folder_path).replace(os.sep, '.'))[0]

                try:
                    module = __import__(f'addons.{module_name}', fromlist=[''])
                except ImportError as e:
                    print(f"Erreur d'importation pour le module {module_name}: {e}")
                    continue

                dict_doc, dict_func, addon_name = module.WebDeckAddon._dict_doc, module.WebDeckAddon._dict_func, module.WebDeckAddon._addon_name
                all_func[addon_name] = dict_func
                dict_doc = {x: y._to_dict() for x, y in dict_doc.items()}
                commands[addon_name] = dict_doc


    random_bg = "//"
    if str(config["front"]["background"]) in ["", [''], []]:
        random_bg = "#141414"
        config["front"]["background"] = ['#141414']
        with open('config.json', 'w', encoding="utf-8") as json_file:
            json.dump(config, json_file, indent=4)
    while random_bg.startswith('//') == True:
        random_bg = random.choice(config["front"]["background"])
        if random_bg.startswith('**uploaded/'):
            random_bg_path = random_bg.replace('**uploaded/', 'static/files/uploaded/')
            if os.path.exists(random_bg_path):
                file_name, extension = os.path.splitext(os.path.basename(random_bg_path))
                random_bg_90_path = f"static/files/uploaded/{file_name}-90{extension}"
                if not os.path.exists(random_bg_90_path):
                    img = Image.open(random_bg_path)
                    img_rotated = img.rotate(-90, expand=True)
                    file_name, extension = os.path.splitext(os.path.basename(random_bg_path))
                    img_rotated.save(random_bg_90_path)
    print(f"random background: {random_bg}")

    themes = [
        file_name
        for file_name in os.listdir("static/themes/")
        if file_name.endswith(".css")
    ]
    
    return render_template("index.jinja",
                            config=config, themes=themes, commands=commands, versions=versions,
                            is_exe=is_exe, langs=['en','fr'], random_bg=random_bg, usage_example=usage_example,
                            int=int, str=str, dict=dict, json=json, type=type, eval=eval, open=open, isfile=os.path.isfile
                            )


@app.route("/config")
@app.route("/settings")
def update_config():
    with open('config.json', encoding="utf-8") as f:
        config_json = json.load(f)
    return render_template("config.html", config=config_json)


def print_dict_differences(dict1, dict2):
    diff = DeepDiff(dict1, dict2, ignore_order=True)
    
    print("Différences trouvées :")
    for key, value in diff.items():
        print(f"Clé : {key}")
        print(f"Différence : {value}")
        print("----------------------")

def merge_dicts(d1, d2):
    """
    Fusionne deux dictionnaires en prenant en compte les sous-dictionnaires.
    Les clés du d2 écrasent les clés correspondantes dans le d1, sauf si elles font partie d'un sous-dictionnaire.
    """
    for key in d2:
        if key in d1 and isinstance(d1[key], dict) and isinstance(d2[key], dict):
            # Récursivement, on fusionne les sous-dictionnaires avec la méthode merge_dict.
            merge_dicts(d1[key], d2[key])
        else:
            # Si la clé existe dans d1 et qu'elle n'est pas un sous-dictionnaire, on la remplace par celle de d2.
            d1[key] = d2[key]
    return d1

folders_to_create = []
@app.route('/save_config', methods=['POST'])
def saveconfig():
    global folders_to_create

    with open('config.json', encoding="utf-8") as f:
        config = json.load(f) 

    # Récupère les données du formulaire
    new_config = request.get_json()
    print(new_config)
    print(config['settings']['show-console'])

    new_height = new_config['front']['height']
    new_width = new_config['front']['width']
    config = update_gridsize(config, new_height, new_width)
    config['front']['height'] = new_height
    config['front']['width'] = new_width

    soundboard_restart = (
        not config['settings']['soundboard']
        == new_config['settings']['soundboard']
    )
    config = check_json_update(config)
    new_config = check_json_update(new_config)


    if config['settings']['windows-startup'].lower().strip() == 'false' and \
                new_config['settings']['windows-startup'].lower().strip() == 'true':
        if getattr(sys, 'frozen', False):
            dir = os.getenv('APPDATA') + r'\Microsoft\Windows\Start Menu\Programs\Startup'
            path = os.path.join(dir, 'WebDeck.lnk')
            target = os.getcwd() + r'\\WebDeck.exe'
            working_dir = os.getcwd()
            icon = os.getcwd() + r'\\WebDeck.exe'

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = working_dir
            shortcut.IconLocation = icon
            shortcut.save()
    elif config['settings']['windows-startup'].lower().strip() == 'true' and \
                new_config['settings']['windows-startup'].lower().strip() == 'false':
        if getattr(sys, 'frozen', False):
            file_path = os.getenv('APPDATA') + r'\Microsoft\Windows\Start Menu\Programs\Startup\WebDeck.lnk'
            if os.path.exists(file_path):
                os.remove(file_path)


    config = merge_dicts(config, new_config)
    config = create_folders(config)
    config = save_config(config)

    try:
        config['front']['background'] = eval(config['front']['background'])
    except TypeError:
        pass

    with open('config.json', 'w', encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)

    if soundboard_restart:
        restart_soundboard()

    print(config['settings']['show-console'])

    return jsonify({'success': True})

# sauvegarde la config ENTIEREMENT, elle ne merge rien
@app.route('/COMPLETE_save_config', methods=['POST'])
def complete_save_config():
    global folders_to_create
    # Récupère les données du formulaire
    old_height = config['front']['height']
    old_width = config['front']['width']
    config = request.get_json()
    new_height = config['front']['height']
    new_width = config['front']['width']
    
    config = create_folders(config)
    config = save_config(config)

    config['front']['height'] = old_height
    config['front']['width'] = old_width
    config = update_gridsize(config, new_height, new_width)
    config['front']['height'] = new_height
    config['front']['width'] = new_width
    with open('config.json', 'w', encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
    
    return jsonify({'success': True})

@app.route('/save_single_button', methods=['POST'])
def save_single_button():
    data = request.get_json()
    button_folder = int(data.get('location_Folder'))
    button_index = int(data.get('location_Id'))
    button_content = data.get('content')
    
    with open('config.json', encoding="utf-8") as f:
        config = json.load(f)
    
    button_folderName = list(config['front']['buttons'])[button_folder]
    print('FETCH /save_single_button -> before :' + str(config['front']['buttons'][button_folderName][button_index]))
    config['front']['buttons'][button_folderName][button_index] = button_content
    print('FETCH /save_single_button -> after  :' + str(config['front']['buttons'][button_folderName][button_index]))
    
    with open('config.json', 'w', encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
    
    return jsonify({'success': True})
    
# sauvegarde la config mais seulement les boutons
@app.route('/save_buttons_only', methods=['POST'])
def save_buttons_only():
    global folders_to_create
    
    # recup config actuelle
    with open('config.json', encoding="utf-8") as f:
        config = json.load(f)

    # Récupère les données du formulaire
    new_config = request.get_json()

    new_config = new_config['front']['buttons']

    temp_order_list = [key for key, value in config['front']['buttons'].items()]
    print(temp_order_list)

    sorted_buttons = {}
    for folder in temp_order_list:
        sorted_buttons[folder] = new_config.get(folder)

    config['front']['buttons'] = sorted_buttons
    config = create_folders(config)
    config = save_config(config)
    return jsonify({'success': True})

@app.route('/get_config', methods=['GET'])
def get_config():
    global folders_to_create
    
    with open('config.json', encoding="utf-8") as f:
        config = json.load(f)
    
    config = create_folders(config)

    with open('config.json', 'w', encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
        
    return jsonify(config)

root = tk.Tk()
root.withdraw()  # Cache la fenêtre principale
root.iconbitmap("static/files/icon.ico")
@app.route('/upload_filepath', methods=['POST'])
def upload_filepath():
    return filedialog.askopenfilename()

@app.route('/upload_file', methods=['POST'])
def upload_file():
    print(request)
    print(request.files)
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Aucun fichier trouvé'})
    
    uploaded_file = request.files['file']
    
    save_path = os.path.join('static/files/uploaded', uploaded_file.filename)
    uploaded_file.save(save_path)

    if request.form.get('info') and request.form.get('info') == "background_image":
        img = Image.open(save_path)
        img_rotated = img.rotate(-90, expand=True)
        file_name, extension = os.path.splitext(os.path.basename(save_path))
        img_rotated.save(f"static/files/uploaded/{file_name}-90{extension}")

    return jsonify({'success': True, 'message': 'Fichier téléchargé avec succès'})

@app.route('/create_folder', methods=['POST'])
def create_folder():
    global folders_to_create
    data = request.get_json()
    folder_name = data.get('name')
    parent_folder_name = data.get('parent_folder')

    if (
        all(item["name"] != folder_name for item in folders_to_create)
        and folder_name not in config['front']['buttons'].keys()
    ):
        folders_to_create.append(
            {
                "name": f"{folder_name}",
                "parent_folder": f"{parent_folder_name}"
            }
        )
        return jsonify({'success': True})
    else:   
        return jsonify({'success': False})

def kill_nircmd():
    try:
        subprocess.Popen("taskkill /f /IM nircmd.exe", shell=True)
    except:
        pass
    
def send_data(message=None):
    global all_func, obs
    
    message = message.replace('<|§|>', ' ')
    
    try: os.remove('temp/mic-temp')
    except: pass
    
    if not message.strip().replace("\n", "").replace("\r", "") == "":
        print('command recieved: ' + message)
    if message.startswith("/debug-send"):
        data = {'message': 'Hello, world!'}
        data = json.loads(message.replace("'",'"').replace("/debug-send",""))
        send(data)
    
    elif message.startswith("/exit"):
        sys.exit("/exit received")


        
    elif message.startswith('/stop_sound'):
        return stop_soundboard()
    elif message.startswith('/playsound '):
        message = message.replace('C:\\fakepath\\', '').replace('/playsound ', '')
        percentage = message[message.rfind(' ') + 1:].replace(' ','')
        try: 
            sound_volume = float(percentage) / 100
            sound_file = message.replace('/playsound ', '').replace(percentage, '')
        except:
            sound_volume = float(50) / 100  # mid volume (default)
            sound_file = message.replace('/playsound ', '')

        if all(substring not in sound_file for substring in [":", "static/files/uploaded/", "static\\files\\uploaded\\"]):
            # si il est stocké directement dans static/files/uploaded et pas dans C:\example
            sound_file = f"static/files/uploaded/{sound_file}"
        
        ear_soundboard = config['settings']["ear-soundboard"].lower() == "true"
        return playsound(sound_file, sound_volume, ear_soundboard)

    elif message.startswith('/playlocalsound '):
        message = message.replace('C:\\fakepath\\', '').replace('/playlocalsound ', '')
        percentage = message[message.rfind(' ') + 1:].replace(' ','')
        try: 
            sound_volume = float(percentage) / 100
            sound_file = message.replace('/playlocalsound ', '').replace(percentage, '')
        except:
            sound_volume = float(50) / 100  # mid volume (default)
            sound_file = message.replace('/playlocalsound ', '')
            
        try:
            player = vlc.MediaPlayer(sound_file)
            player.audio_set_volume(int(sound_volume * 100))
            player.play()
            player.event_manager().event_attach(
                vlc.EventType.MediaPlayerEndReached, lambda x: remove_player(3, player)
            )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(f"{exc_type} | {e} | {fname} | python line: {exc_tb.tb_lineno}")
            print("ERROR:      ", e)
            print("ERROR LINE: ", exc_tb.tb_lineno)
            print2("Error while loading MP3 file named " + sound_file)

    elif message.startswith('/exec'):
        exec(message.replace('/exec', '').strip())

    elif message.startswith('/batch'):
        subprocess.Popen(message.replace('/batch', '', 1).strip(), shell=True)

    elif message.startswith(('/openfile', '/start')):
        path = message.replace('/openfile', '', 1).replace('/start', '', 1).strip()
        
        if ':' in path:
            initial_path = os.getcwd()
            try:
                file_directory = os.path.dirname(path)
                os.chdir(file_directory)
                os.startfile(path)
            finally:
                os.chdir(initial_path)
        else:
            os.startfile(path)


    elif message.startswith('/PCshutdown'):
        subprocess.Popen('shutdown /s /f /t 0', shell=True)
    
    elif message.startswith('/PCrestart'):
        subprocess.Popen('shutdown /r /f /t 0', shell=True)
    
    elif message.startswith('/PCsleep'):
        subprocess.Popen('rundll32.exe powrprof.dll,SetSuspendState 0,1,0', shell=True)
    
    elif message.startswith('/PChibernate'):
        subprocess.Popen('shutdown /h /t 0', shell=True)
    
    elif message.startswith('/locksession'):
        subprocess.Popen('Rundll32.exe user32.dll,LockWorkStation', shell=True)

    elif message.startswith('/screensaversettings'):
        subprocess.Popen('rundll32.exe desk.cpl,InstallScreenSaver toasters.scr', shell=True)

    elif message.startswith('/screensaver') and not message.startswith('/screensaversettings'):
        if message.endswith(('on', '/screensaver', 'start')):
            subprocess.Popen('%windir%\system32\scrnsave.scr /s', shell=True)

        elif message.endswith(('hard', 'full', 'black')):
            subprocess.Popen('nircmd.exe monitor off', shell=True)
            kill_nircmd()

        elif message.endswith(('off', 'false')):
            keyboard.press('CTRL')

    elif message.startswith('/key'):
        key = message.replace('/key', '', 1).strip()
        keyboard.press(key)

    elif message.startswith('/restartexplorer'):
        subprocess.Popen('taskkill /f /im explorer.exe', shell=True)
        time.sleep(0.5)
        subprocess.Popen('explorer.exe', shell=True)
        hwnd = get_window_by_name('explorer.exe')
        if hwnd:
            close_window(hwnd)

    elif message.startswith(('/kill', '/taskill', '/taskkill', '/forceclose')):
        window_name = message.replace('/kill', '').replace('/taskill', '').replace('/taskkill', '').replace('/forceclose', '')
        hwnd = get_window_by_name(window_name)
        if hwnd:
            print(f"Fenêtre '{window_name}' trouvée avec handle : {hwnd}")
        else:
            print(f"Fenêtre '{window_name}' non trouvée")
        try:
            close_window(hwnd)
        except:
            if not '.' in window_name:
                window_name += '.exe'
            subprocess.Popen(f'taskkill /f /im {window_name}', shell=True)

    elif message.startswith('/restart'):
        exe = message.replace('/restart', '')
        if not '.' in exe:
            exe += '.exe'
        subprocess.Popen(f'taskkill /f /im {exe}', shell=True)
        subprocess.Popen(f'start {exe}', shell=True)

    elif message.startswith('/clearclipboard'):
        subprocess.Popen('cmd /c "echo off | clip"', shell=True)

    elif message.startswith('/write '):
        keyboard2.write(message.replace('/write ', ''))

    elif message.startswith('/writeandsend '):
        keyboard2.write(message.replace('/writeandsend ', ''))
        keyboard2.press('ENTER')

    elif message.startswith('/volume +'):
        delta = message.replace('/volume +', '')
        if delta.strip() == "":
            increase_volume("1")
        else:
            increase_volume(delta)
    elif message.startswith('/volume -'):
        delta = message.replace('/volume -', '')
        if delta.strip() == "":
            decrease_volume(delta)
        else:
            decrease_volume("1")
    elif message.startswith('/volume set'):
        target_volume = int(message.replace('/volume set ', '')) / 100.0
        set_volume(target_volume)

    elif message.startswith(('/appvolume +', '/appvolume -', '/appvolume set')):
        comtypes.CoInitialize()
        command = message.replace('/appvolume ', '').replace('set ', 'set').split()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name().lower() == command[1].lower():
                print("Current volume: %s" % volume.GetMasterVolume())
                old_volume = volume.GetMasterVolume()
                old_volume_percent = round(old_volume * 100)

                if command[0].startswith('set'):
                    target_volume = int(command[0].replace('set', ''))
                    if target_volume > 100:
                        target_volume = 100
                    if target_volume < 0:
                        target_volume = 0
                elif command[0].startswith('+'):
                    if command[0].replace('+', '') == '':
                        target_volume = old_volume_percent + 1
                    else:
                        target_volume = old_volume_percent + \
                            int(command[0].replace('+', ''))
                elif command[0].startswith('-'):
                    if command[0].replace('-', '') == '':
                        target_volume = old_volume_percent - 1
                    else:
                        target_volume = old_volume_percent - \
                            int(command[0].replace('-', ''))
                target_volume_float = target_volume / 100.0

                volume.SetMasterVolume(target_volume_float, None)
                print("New volume: %s" % volume.GetMasterVolume())

        comtypes.CoUninitialize()

    elif message.startswith('/soundcontrol mute'):
        keyboard.press('volumemute')
    elif message.startswith('/mediacontrol playpause'):
        keyboard.press('playpause')
    elif message.startswith('/mediacontrol previous'):
        keyboard.press('prevtrack')
    elif message.startswith('/mediacontrol next'):
        keyboard.press('nexttrack')

    elif message.startswith('/spotify likealbum'):
        sp = spotipy.Spotify(auth=spotify_token)
        # Get information about the user's currently playing track
        track_info = sp.current_playback()

        # If a track is currently playing, like it
        if track_info is not None:
            album_id = track_info['item']['album']['id']

            is_liked = sp.current_user_saved_albums_contains(albums=[album_id])[0]
            # Add or remove like based on current state
            if is_liked:
                sp.current_user_saved_albums_delete(albums=[album_id])
                print(f"Removed album {track_info['item']['album']['name']} by {track_info['item']['album']['artists'][0]['name']}")
            else:
                sp.current_user_saved_albums_add(albums=[album_id])
                print(f"Liked album {track_info['item']['album']['name']} by {track_info['item']['album']['artists'][0]['name']}")
        else:
            print("No album currently playing.")

    elif message.startswith('/spotify playsong'):
        song_name = message.replace('/spotify playsong','').strip()
        
        sp = spotipy.Spotify(auth=spotify_token)
        results = sp.search(song_name, 1, 0, "track")
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])

    elif message.startswith('/spotify playplaylist'):
        playlist_name = message.replace('/spotify playplaylist', '').strip()
        
        sp = spotipy.Spotify(auth=spotify_token)
        playlists = sp.current_user_playlists()  # Récupérer les playlists de l'utilisateur actuel
        
        for playlist in playlists['items']:
            if playlist_name.lower().strip() in playlist['name'].lower().strip():
                playlist_uri = playlist['uri']
                sp.start_playback(context_uri=playlist_uri)
                break
        else:
            print(f"Playlist '{playlist_name}' non trouvée.")
    
    elif message.startswith('/spotify likesong'):
        sp = spotipy.Spotify(auth=spotify_token)
        # Get information about the user's currently playing track
        track_info = sp.current_playback()

        # If a track is currently playing, like it
        if track_info is not None:
            track_id = track_info['item']['id']
            print(track_info)

            is_liked = sp.current_user_saved_tracks_contains(tracks=[track_id])[0]
            # Add or remove like based on current state
            if is_liked:
                sp.current_user_saved_tracks_delete(tracks=[track_id])
                print(f"Removed track {track_info['item']['name']} by {track_info['item']['artists'][0]['name']}")
            else:
                sp.current_user_saved_tracks_add(tracks=[track_id])
                print(f"Liked track {track_info['item']['name']} by {track_info['item']['artists'][0]['name']}")
        else:
            print("No track currently playing.")

    elif message.startswith(('/spotify add_to_playlist', '/spotify remove_from_playlist', '/spotify add_or_remove')):
        playlist_name = message.replace('/spotify add_to_playlist', '').replace(
            '/spotify remove_from_playlist', '').replace('/spotify add_or_remove', '').strip()
        sp = spotipy.Spotify(auth=spotify_token)
        playlists = sp.current_user_playlists()
        playlist_id = None

        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                break

        if playlist_id is None:
            print2(f"Playlist named '{playlist_name}' not found.")
        else:
            playback = sp.current_playback()
            track_id = playback['item']['id']
            track_uri = playback['item']['uri']
            if 'add_or_remove' in message:
                playlist_items = sp.playlist_items(
                    playlist_id, fields='items(track(uri))')
                track_uris = [item['track']['uri'] for item in playlist_items['items']]

                if track_uri in track_uris:
                    sp.playlist_remove_all_occurrences_of_items(
                        playlist_id, [track_uri])
                    print("La piste a été retirée de la playlist.")
                else:
                    sp.playlist_add_items(playlist_id, [track_id])
                    print("La piste a été ajoutée à la playlist.")
            elif 'add_to_playlist' in message:
                sp.playlist_add_items(playlist_id, [track_id])
            elif 'remove_from_playlist' in message:
                sp.playlist_remove_all_occurrences_of_items(
                    playlist_id, [track_uri])

    elif message.startswith(('/spotify follow_artist', '/spotify unfollow_artist', '/spotify follow_or_unfollow_artist')):
        artist = message.replace('/spotify follow_artist', '').replace(
            '/spotify unfollow_artist', '').replace('/spotify follow_or_unfollow_artist', '').strip()
        sp = spotipy.Spotify(auth=spotify_token)
        playback = sp.current_playback()
        artist_id = playback['item']['artists'][0]['id']
        artist_name = playback['item']['artists'][0]['name']
        if 'follow_or_unfollow_artist' in message:
            results = sp.search(q=artist_name, type="artist")
            items = results["artists"]["items"]
            if len(items) > 0:
                artist_id = items[0]["id"]
            else:
                print(f"Impossible de trouver l'artiste '{artist_id}' sur Spotify.")

            # Vérifier si l'utilisateur est abonné à l'artiste correspondant
            response = sp.current_user_following_artists(ids=[artist_id])
            is_following = response[0]

            if is_following:
                print(f"L'utilisateur est abonné à l'artiste '{artist_id}'.")
                sp.user_unfollow_artists([artist_id])
                print("L'artiste a bien été retiré de la liste d'abonnements.")
            else:
                print(
                    f"L'utilisateur n'est pas abonné à l'artiste '{artist_id}'.")
                sp.user_follow_artists([artist_id])
                print("L'artiste a bien été ajouté à la liste d'abonnements.")

        elif 'unfollow_artist' in message:
            sp.user_unfollow_artists([artist_id])
            print("L'artiste a bien été retiré de la liste d'abonnements.")
        elif 'follow_artist' in message:
            sp.user_follow_artists([artist_id])
            print("L'artiste a bien été ajouté à la liste d'abonnements.")

    elif message.startswith(('/spotify volume +', '/spotify volume -', '/spotify volume set')):
        sp = spotipy.Spotify(auth=spotify_token)
        # Get the current playback information
        playback_info = sp.current_playback()

        # Check if there is an active device
        if playback_info and playback_info['is_playing'] and playback_info['device']:
            device_id = playback_info['device']['id']
        else:
            print("No active device found.")

        # Get the current volume
        current_volume = playback_info['device']['volume_percent']
        print(f"Current volume: {current_volume}")

        if '-' in message:
            try:
                target_volume = current_volume - int(message.replace('/spotify volume -', ''))
            except:
                target_volume = current_volume - 10
        elif '+' in message:
            try:
                target_volume = current_volume + int(message.replace('/spotify volume +', ''))
            except:
                target_volume = current_volume + 10
        elif 'set' in message:
            try:
                target_volume = int(message.replace('/spotify volume set', ''))
            except:
                target_volume = current_volume
                print2('Error, unable to apply volume')
        if isinstance(target_volume, int):
            if target_volume > 100:
                target_volume = 100
            if target_volume < 0:
                target_volume = 0
            target_volume = int(target_volume)
            try:
                sp.volume(target_volume, device_id=device_id)
            except:
                print2('Error, unable to apply volume because Spotify Prenium is required')

            # Get the updated volume
            playback_info = sp.current_playback()
            current_volume = playback_info['device']['volume_percent']
            print(f"Updated volume: {current_volume}")
        else:
            print("Volume must be an integer")

    elif message.startswith('/speechrecognition'):
        keyboard.hotkey('win', 'h')

    # /colorpicker lang:en type:text|name;text-original|name-original;hex;rgb;hsl copy:text;hex;rgb;hsl copytype:raw|list showtype:raw|list remove_hex_sharp:false
    elif message.startswith('/colorpicker'):

        x, y = keyboard.position()

        # Obtient la capture d'écran de chaque moniteur et compare la position du curseur pour déterminer l'écran
        for i, monitor in enumerate(mss.mss().monitors):
            if monitor["left"] <= x < monitor["left"] + monitor["width"] and \
                    monitor["top"] <= y < monitor["top"] + monitor["height"]:
                monitor_index = i
                break

        # Capturer la capture d'écran de l'écran spécifique
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_index]
            img = sct.grab(monitor)
            screenshot = np.array(Image.frombytes(
                'RGB', img.size, img.bgra, 'raw', 'BGRX'))

        # Obtient la couleur du pixel sous le curseur de la souris
        color = screenshot[y - monitor["top"], x - monitor["left"]]

        # Convertit la couleur en format HEX
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)

        # Convertit la couleur en format RGB
        rgb_color = 'rgb({},{},{})'.format(*color)

        # Convertit la couleur en format HSL
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

        hsl_color = 'hsl({}, {:.2f}%, {:.2f}%)'.format(
            hue, saturation * 100, lightness * 100)

        target_language = getarg(message, 'lang')
        selectedtypes = getarg(message, 'type')
        typestocopy = getarg(message, 'copy')
        copytype = getarg(message, 'copytype')
        showtype = getarg(message, 'showtype')
        try:
            remove_hex_sharp = getarg(message, 'remove_hex_sharp').capitalize()
        except AttributeError:
            remove_hex_sharp = None
        print('------------------------------------------')
        print(target_language)
        print(selectedtypes)
        print(typestocopy)
        print(copytype)
        print(showtype)
        print(remove_hex_sharp)
        print('------------------------------------------')

        with open('colors.json', 'r', encoding="utf-8") as f:
            colorsjson = json.load(f)
        if target_language is None or target_language == 'en':
            named_original = find_color(hex_color, colorsjson)
            named_color = named_original
        else:
            named_original = find_color(hex_color, colorsjson)
            named_color = translate(named_original, target_language)

        types_found = {
            "NAME":named_color,
            "TEXT":named_color,
            "NAME-ORIGINAL":named_original,
            "TEXT-ORIGINAL":named_original,
            "HEX":hex_color,
            "RGB":rgb_color,
            "HSL":hsl_color
        }
        
        
        types_found_final = {}
        if selectedtypes:
            for type in selectedtypes.split(';'):
                for type_found, value in types_found.items():
                    if type.upper() in type_found:
                        if 'HEX' in type.upper() and remove_hex_sharp == 'True':
                                types_found_final[type.upper()] = value.replace('#','')
                        else:
                            types_found_final[type.upper()] = value
            print(types_found_final)
        else:
            for type_found, value in types_found.items():
                if not any(elem in type_found for elem in ['TEXT', 'ORIGINAL']):
                    types_found_final[type_found] = value
            print(types_found_final)

        # copy:text;hex;rgb;hsl copytype:raw|list
        typestocopy_final = {}
        if typestocopy:
            for type in typestocopy.split(';'):
                for type_found, value in types_found.items():
                    if type.upper() in type_found:
                        if 'HEX' in type.upper() and remove_hex_sharp == 'True':
                            typestocopy_final[type.upper()] = value.replace('#','')
                        else:
                            typestocopy_final[type.upper()] = value
            if copytype.lower() == 'list':
                if len(typestocopy.split(';')) == 1:
                    pyperclip.copy(str(typestocopy_final)[:-2][2:].replace("'",''))
                else:
                    pyperclip.copy(str(typestocopy_final).replace("', ",',\n')[:-2][2:].replace("'",''))
            else:
                if len(typestocopy.split(';')) == 1:
                    pyperclip.copy(list(typestocopy_final.values())[0])
                else:
                    pyperclip.copy(', '.join(typestocopy_final.values()))
        
        
        title = "WebDeck Color Picker"
        icon = "static\\files\\icon.ico"
        duration = 5
        message = ''
        if showtype and showtype.lower() != 'list':
            if typestocopy and len(typestocopy.split(';')) == 1:
                message = list(types_found_final.values())[0]
            else:
                message = ', '.join(types_found_final.values())
        else:
            if typestocopy and len(typestocopy.split(';')) == 1:
                message = str(types_found_final)[:-2][2:].replace("'",'')
            else:
                message = str(types_found_final).replace("', ",',\n')[:-2][2:].replace("'",'')

        toaster.show_toast(title, message, icon_path=icon, duration=duration, threaded=True)

    elif message.startswith('/superAltF4'):
        hwnd = get_focused_window()
        if hwnd:
            close_window(hwnd)
            subprocess.Popen(f'taskkill /f /im {hwnd}', shell=True)
            subprocess.Popen(f'taskkill /f /im {hwnd}.exe', shell=True)

    # A FIX
    elif message.startswith('/firstplan'):
        window_name = message.replace('/firstplan','').strip()
        
        hwnd = get_window_by_name(window_name)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            keyboard2.press('ENTER')
            print(f"Fenêtre '{window_name}' mise au premier plan")
        else:
            print(f"Fenêtre '{window_name}' non trouvée")

    elif message.startswith('/setmicrophone'):
        set_microphone_by_name(message.replace('/setmicrophone','').strip())
        # PAS FINI
    elif message.startswith('/setoutputdevice'):
        set_speakers_by_name(message.replace('/setoutputdevice','').strip())
        # PAS FINI

    elif message.startswith('/copy'):
        if message.strip() == '/copy':
            keyboard.hotkey('ctrl', 'c')
        else:
            msg = message.replace('/copy ','',1)
            if msg.startswith('/copy'):
                msg = message.replace('/copy','',1)
            pyperclip.copy(msg)
            
    elif message.startswith('/paste'):
        if message.strip() == '/paste':
            keyboard.hotkey('ctrl', 'v')
        else:
            msg = message.replace('/paste ','',1)
            if msg.startswith('/paste'):
                msg = message.replace('/paste','',1)
            pyperclip.copy(msg)
            keyboard.hotkey('ctrl', 'v')
    
    elif message.startswith('/cut'):
        keyboard.hotkey('ctrl', 'x')
            
    elif message.startswith('/clipboard'):
        keyboard.hotkey('win', 'v')
    
    
    # OBS  -  https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md
    #         https://github.com/Elektordi/obs-websocket-py
    
    if message.startswith('/obs_'):
        try:
            obs = obsws(obs_host, obs_port, obs_password)
            obs.connect()
        except:
            return jsonify({"success": False, "message": "Failed connection to obs."})
    
    
        if message.startswith('/obs_scene'):
            scene_name = message.replace('/obs_scene','').lower().strip()
            
            scenes = obs.call(obsrequests.GetSceneList())
            for scene in scenes.getScenes():
                if scene['sceneName'].lower().strip() == scene_name:    
                    print(f"Switching to {scene['sceneName']}")
                    obs.call(obsrequests.SetCurrentProgramScene(sceneName=scene['sceneName']))
            
        
        elif message.startswith('/obs_toggle_rec'):
            result = obs.call(obsrequests.ToggleRecord())
            print("Recording toggled successfully.")
            if 'failed' in str(result):
                return jsonify({"success": False, "message": "Failed :/"})
            
        elif message.startswith('/obs_start_rec'):
            recording_status = obs.call(obsrequests.GetRecordStatus())
            if recording_status.getOutputActive():
                print("OBS is already recording.")
                return jsonify({"success": False, "message": "OBS is already recording."})
            else:
                obs.call(obsrequests.StartRecord())
                print("Recording started successfully.")
        
        elif message.startswith('/obs_stop_rec'):
            recording_status = obs.call(obsrequests.GetRecordStatus())
            if recording_status.getOutputActive():
                obs.call(obsrequests.StopRecord())
                print("Recording stopped successfully.")
            else:
                print("OBS is not recording.")
                return jsonify({"success": False, "message": "OBS is not recording."})
            
        
        elif message.startswith('/obs_toggle_rec_pause'):
            result = obs.call(obsrequests.ToggleRecordPause())
            print("Play/pause toggled successfully.")
            if 'failed' in str(result):
                return jsonify({"success": False, "message": "Failed :/"})
                
        elif message.startswith('/obs_pause_rec'):
            recording_status = obs.call(obsrequests.GetRecordStatus())
            if recording_status.getOutputActive():
                result = obs.call(obsrequests.PauseRecord())
                print(result)
                if 'failed' in str(result):
                    return jsonify({"success": False, "message": "No recording can be paused"})
            else:
                return jsonify({"success": False, "message": "No recording can be paused"})
                
        elif message.startswith('/obs_resume_rec'):
            result = obs.call(obsrequests.ResumeRecord())
            print(result)
            if 'failed' in str(result):
                return jsonify({"success": False, "message": "No recording is paused"})
                
        
        elif message.startswith('/obs_toggle_stream'):
            result = obs.call(obsrequests.ToggleStream())
            print("Streaming toggled successfully.")
            if 'failed' in str(result):
                return jsonify({"success": False, "message": "Failed :/"})        
        
        elif message.startswith('/obs_start_stream'):
            recording_status = obs.call(obsrequests.GetStreamStatus())
            if recording_status.getOutputActive():
                print("OBS is already streaming.")
                return jsonify({"success": False, "message": "OBS is already streaming."})
            else:
                obs.call(obsrequests.StartStream())
                print("Stream started successfully.")
        
        elif message.startswith('/obs_stop_stream'):
            recording_status = obs.call(obsrequests.GetStreamStatus())
            if recording_status.getOutputActive():
                obs.call(obsrequests.StopStream())
                print("Stream stopped successfully.")
            else:
                print("OBS is not streaming.")
                return jsonify({"success": False, "message": "OBS is not streaming."})
        
        
        elif message.startswith('/obs_toggle_virtualcam'):
            result = obs.call(obsrequests.ToggleVirtualCam())
            print("Virtual cam toggled successfully.")
            if 'failed' in str(result):
                return jsonify({"success": False, "message": "Failed :/"})        
        
        elif message.startswith('/obs_start_virtualcam'):
            recording_status = obs.call(obsrequests.GetVirtualCamStatus())
            print(recording_status)
            if recording_status.getOutputActive():
                print("Virtual cam is already started.")
                return jsonify({"success": False, "message": "Virtual cam is already started."})
            else:
                obs.call(obsrequests.StartVirtualCam())
                print("Virtual cam started successfully.")
        
        elif message.startswith('/obs_stop_virtualcam'):
            recording_status = obs.call(obsrequests.GetVirtualCamStatus())
            if recording_status.getOutputActive():
                obs.call(obsrequests.StopVirtualCam())
                print("Virtual cam stopped successfully.")
            else:
                print("Virtual cam is already stopped.")
                return jsonify({"success": False, "message": "Virtual cam is already stopped."})
        
        obs.disconnect()


    return jsonify({"success": True})

    
@socketio.event
def send(data):
    socketio.emit('json_data', data)
    
@socketio.on('connect')
def socketio_connect():
    print('Client connected')
    with open('config.json', encoding="utf-8") as f:
        config = json.load(f)
    
    
@socketio.on('message_from_socket')
def send_data_socketio(message):
    return send_data(message=message)

@app.route('/send-data', methods=['POST'])
def send_data_route():
    return send_data(message=request.get_json()["message"])


try:
    os.remove('temp/mic-temp')
except:
    pass

def compare_versions(version1, version2):
    v1_components = list(map(int, version1.split('.')))
    v2_components = list(map(int, version2.split('.')))
    
    for v1, v2 in zip(v1_components, v2_components):
        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
    
    if len(v1_components) > len(v2_components):
        return 1
    elif len(v1_components) < len(v2_components):
        return -1
    
    return 0

def check_for_updates():
    with open('static/files/version.json', encoding="utf-8") as f:
        current_version = json.load(f)['versions'][0]['version']
    response = requests.get("https://raw.githubusercontent.com/LeLenoch/WebDeck/master/static/files/version.json")
    data = response.json()
    
    files_to_update = []
    for version_data in reversed(data["versions"]):
        version = version_data["version"]
        if compare_versions(version, current_version) > 0:
            print(f"New version available: {version}")
            try:
                subprocess.Popen(['WD_updater.exe'])
            except:
                pass
            
            break
        
def check_for_updates_loop():
    while True:
        
        with open('config.json', encoding="utf-8") as f:
            config = json.load(f)
        if 'auto-updates' in config['settings'].keys():
            if config['settings']['auto-updates'].lower().strip() == 'true':
                check_for_updates()
        else:
            config['settings']['auto-updates'] = 'true'
            check_for_updates()
        with open('config.json', 'w', encoding="utf-8") as json_file:
            json.dump(config, json_file, indent=4)
        
        time.sleep(3600)

def auto_closing_loop():
    print('main_server started')
    while True:
        should_i_close()
        time.sleep(5)

# mic to vbcable
sb_on = True
def soundboard():
    global sb_on
    sb_on = True

    audio = pyaudio.PyAudio()
    num_devices = audio.get_device_count()
    
    mic_input_device = config['settings']['soundboard']['mic_input_device']
    microphone_name = mic_input_device[mic_input_device.find("(") + 1:]
    mic_output_device = config['settings']['soundboard']['vbcable']
    output_name = mic_output_device[mic_output_device.find("(") + 1:]
    mic_index = None
    output_device = None
    
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0 and microphone_name.lower() in device_info['name'].lower():
            mic_index = i
            break
    
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info['maxOutputChannels'] > 0 and output_name.lower() in device_info['name'].lower():
            output_device = i
            break
    
    if mic_index is None:
        print("Impossible de trouver le microphone.")
    else:
        print(f"Microphone '{microphone_name}' found at index {mic_index}")
    
    if output_device is None:
        print("Impossible de trouver les haut-parleurs.")
    else:
        print(f"Speaker '{output_name}' found at index {output_device}")
    
    stream_in = None
    stream_out = None
    
    input_device_info = audio.get_device_info_by_index(mic_index)
    input_channels = input_device_info['maxInputChannels']
    
    output_device_info = audio.get_device_info_by_index(output_device)
    output_channels = input_device_info['maxInputChannels']
    
    print(f"i: {input_device_info}")
    print(f"o: {output_device_info}")
    
    stream_in = audio.open(format=pyaudio.paInt16,
                            channels=input_channels,
                            rate=44100,
                            input=True,
                            input_device_index=mic_index)
    
    stream_out = audio.open(format=pyaudio.paInt16,
                            channels=input_channels,
                            rate=44100,
                            output=True,
                            output_device_index=output_device)
    
    print("soundboard: ON")
    
    try:
        while sb_on == True:
            data = stream_in.read(1024)
            stream_out.write(data)
    except KeyboardInterrupt:
        pass
    finally:
        print("Arrêt de la soundboard.")
    
        if stream_in is not None:
            stream_in.stop_stream()
            stream_in.close()
    
        if stream_out is not None:
            stream_out.stop_stream()
            stream_out.close()
    
        audio.terminate()

def restart_soundboard():
    global soundboard_thread, sb_on
    sb_on = False
    time.sleep(0.2)
    soundboard_thread = threading.Thread(target=soundboard, daemon=True)
    soundboard_thread.start()
    print('sb thread revived')


auto_closing_loop_thread = threading.Thread(target=auto_closing_loop, daemon=True)
soundboard_thread = threading.Thread(target=soundboard, daemon=True)

auto_closing_loop_thread.start()
soundboard_thread.start()

check_for_updates()

def check_firewall_permission():
    try:
        firewall_manager = Dispatch("HNetCfg.FwMgr")
        policy = firewall_manager.LocalPolicy.CurrentProfile
        authorized_applications = policy.AuthorizedApplications

        for app in authorized_applications:
            if app.ProcessImageFileName.lower() == sys.executable.lower():
                print(f"L'application ({sys.executable}) a l'autorisation de passer à travers le pare-feu.")
                return True

        print(f"L'application ({sys.executable}) n'a pas l'autorisation de passer à travers le pare-feu.")
        return False
    except Exception as e:
        print(f"Erreur lors de la vérification du pare-feu : {e}")
        return True

if check_firewall_permission() == False:
    command = [
        'powershell',
        '-NoProfile',
        '-WindowStyle', 'Hidden',
        'New-NetFirewallRule',
        '-DisplayName', '"WebDeck"',
        '-Direction', 'Inbound',
        '-Program', f'"{sys.executable}"',
        '-Action', 'Allow'
    ]
    subprocess.run(command)

app.run(host=local_ip, port=config['url']['port'],
        debug=config['settings']['flask-debug'],
        use_reloader=config['settings']['flask-debug'] == 'false')
obs.disconnect()
import inspect, json,subprocess,sys,time

import comtypes
import keyboard
import pyautogui
import pyperclip
import win32gui
from flask import jsonify
from pycaw.pycaw import (AudioUtilities, IAudioEndpointVolume,
                         ISimpleAudioVolume)


from ..utils.settings.get_config import get_port, get_config
from ..utils.settings.save_config import save_config

from app.utils.logger import log

from . import window
from .usage import extract_asked_device, get_usage

def delete_folder(message):
    config = get_config()
    folders = config["front"]["buttons"]
    
    if len(folders) == 1 and message in folders:
        return
    for folder_name,buttons in folders.copy().items():
        if folder_name == message:
            folders.pop(folder_name)
            log.info(f"Removed folder {folder_name}")
        else:
            for id,button in enumerate(buttons):             
                if "message" in button and button["message"] == f"/folder {message}":                    
                    folders[folder_name][id] = {"VOID": "VOID"}
    config["front"]["buttons"] = folders
    save_config(config)
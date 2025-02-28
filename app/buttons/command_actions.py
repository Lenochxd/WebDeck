import json
import sys
import subprocess
import time
import inspect
from flask import jsonify

import win32gui
import pyperclip
import pyautogui
import keyboard

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import comtypes


from app.utils.logger import log
from app.utils.global_variables import get_global_variable
from app.utils.kill_nircmd import kill_nircmd

from app.utils.firewall import fix_firewall_permission
from .usage import extract_asked_device, get_usage
from . import audio
from . import window
from . import exec
from . import soundboard
from . import spotify
from . import obs
from . import color_picker
from . import system

def restart_explorer():
    subprocess.Popen("taskkill /f /im explorer.exe", shell=True)
    time.sleep(0.5)
    subprocess.Popen("explorer.exe", shell=True)
    hwnd = window.get_by_name("explorer.exe")
    if hwnd:
        window.close(hwnd)

def handle_device_usage(message):
    asked_device = []

    device = extract_asked_device(message)
    if device is not None:
        asked_device.append(device)

    log.debug(f"Asked device: {asked_device}")
    usage = get_usage(False, asked_device)
    log.debug(f"Usage data: {usage}")
    
    return jsonify(usage)


def killtask(message):
    window_name = message.split(maxsplit=1)[-1]  # Extrae el nombre del proceso/ventana
    hwnd = window.get_by_name(window_name)

    if hwnd:
        log.debug(f"Window '{window_name}' found with handle: {hwnd}")
        try:
            window.close(hwnd)
            return
        except:
            pass  # Si falla, continúa con el método alternativo

    log.debug(f"Window '{window_name}' not found, trying taskkill")
    if "." not in window_name:
        window_name += ".exe"    
    subprocess.Popen(f"taskkill /f /im {window_name}", shell=True)

def restarttask(message):
        exe = message.replace("/restart", "")
        if not "." in exe:
            exe += ".exe"
            subprocess.Popen(f"taskkill /f /im {exe}", shell=True)
            subprocess.Popen(f"start {exe}", shell=True)

def adjust_app_volume(message):
    comtypes.CoInitialize()
    command = message.replace("/appvolume ", "").replace("set ", "set").split()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name().lower() == command[1].lower():
            log.debug("Current volume: %s" % volume.GetMasterVolume())
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
            log.debug("New volume: %s" % volume.GetMasterVolume())

    comtypes.CoUninitialize()


def clipboard_action(message):
    if message.startswith("/copy") or message.startswith("/paste"):
        action = message.split(" ")[0][1:]  # Obtener 'copy' o 'paste'
        msg = message[len(f"/{action}"):].strip()  # Obtener el mensaje después del comando
        
        if not msg:
            pyautogui.hotkey("ctrl", "c" if action == "copy" else "v")  # Ejecutar Ctrl+C o Ctrl+V
        else:
            if msg.startswith(f"/{action}"):
                msg = msg[len(f"/{action}"):]  # Eliminar el comando adicional
            pyperclip.copy(msg)  # Copiar al portapapeles
            pyautogui.hotkey("ctrl", "c" if action == "copy" else "v")  # Ejecutar Ctrl+C o Ctrl+V


def bring_window_to_foreground(message):
    window_name = message.replace("/firstplan", "").strip()

    hwnd = window.get_by_name(window_name)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        keyboard.press("ENTER")
        log.success(f"Window '{window_name}' has been brought to the foreground")
    else:
        log.error(f"Window '{window_name}' not found")
        raise RuntimeError(f"Window '{window_name}' not found")


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
from . import command_actions



def handle_command(message: str = None):
    global all_func

    command_arguments = message
    message = message.replace("<|§|>", " ").replace("\n", "").replace("\r", "")
    if message: log.info(f"Command received: {message}")
    
    command_map ={
        "/debug-send":              lambda: log.info("Debug message sent"),
        "/bypass-windows-firewall": lambda: fix_firewall_permission(),
        "/exit" :                   lambda: sys.exit("/exit received"),
        "/stop_sound":              lambda: soundboard.stopsound(),
        "/PCshutdown":              lambda: subprocess.Popen("shutdown /s /f /t 0", shell=True),
        "/PCrestart":               lambda: subprocess.Popen("shutdown /r /f /t 0", shell=True),
        "/PCsleep":                 lambda: subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True),
        "/PChibernate":             lambda: subprocess.Popen("shutdown /h /t 0", shell=True),
        "/locksession":             lambda: subprocess.Popen("Rundll32.exe user32.dll,LockWorkStation", shell=True),
        "/screensaversettings" :    lambda: subprocess.Popen("rundll32.exe desk.cpl,InstallScreenSaver toasters.scr", shell=True),
        "/clearclipboard":          lambda: subprocess.Popen('cmd /c "echo off | clip"', shell=True),
        "/soundcontrol mute":       lambda: pyautogui.press("volumemute"),
        "/mediacontrol playpause":  lambda: pyautogui.press("playpause"),
        "/mediacontrol previous":   lambda: pyautogui.press("prevtrack"),
        "/mediacontrol next":       lambda: pyautogui.press("nexttrack"),
        "/speechrecognition":       lambda: pyautogui.hotkey("win", "h"),
        "/cut":                     lambda: pyautogui.hotkey("ctrl", "x"),
        "/clipboard":               lambda: pyautogui.hotkey("win", "v"),
        "/restartexplorer":         lambda: command_actions.restart_explorer(),

        "/key":                     lambda message: pyautogui.press(message.replace("/key", "", 1).strip()),
        "/delete_folder":           lambda message: command_actions.delete_folder(message.replace("/delete_folder ", "")),
        "/writeandsend":            lambda message: (keyboard.write(message.replace("/writeandsend ","")) or keyboard.press("ENTER")),
        "/write":                   lambda message: keyboard.write(message.replace("/write ", "")),
        "/setmicrophone":           lambda message: audio.set_microphone_by_name(message.replace("/setmicrophone", "").strip()),
        "/setoutputdevice":         lambda message: audio.set_speakers_by_name(message.replace("/setoutputdevice", "").strip()),
        "/usage" :                  lambda message: command_actions.handle_device_usage(message),
        "/restart":                 lambda message: command_actions.restarttask(message),
        "/volume":                  lambda message: audio.change_volume(message),
        "/spotify":                 lambda message: spotify.handle_command(message),
        "/obs":                     lambda message: obs.handle_command(message),
        "/colorpicker":             lambda message: color_picker.handle_command(message),
        "/exec":                    lambda message: exec.python(message),
        "/batch":                   lambda message: exec.batch(message),
        "/firstplan":               lambda message: command_actions.bring_window_to_foreground(message),

        ("/playsound", "/playlocalsound"):                      lambda message : soundboard.playsound(*soundboard.get_params(message)),
        ("/kill", "/taskill", "/taskkill", "/forceclose"):      lambda message: command_actions.killtask(message),
        ("/appvolume +", "/appvolume -", "/appvolume set"):     lambda message: command_actions.adjust_app_volume(message),
        ("/copy","/paste"):                                     lambda message: command_actions.clipboard_action(message),
        ("/openfolder", "/opendir","/openfile", "/start"):      lambda message: system.handle_command(message),



        "/screensaver": lambda message: (
            subprocess.Popen("%windir%\system32\scrnsave.scr /s", shell=True) if message.endswith(("on", "/screensaver", "start")) else
            (subprocess.Popen('"lib/nircmd.exe" monitor off', shell=True) and kill_nircmd() if message.endswith(("hard", "full", "black")) else
            pyautogui.press("CTRL") if message.endswith(("off", "false")) else None)
        ),
        "/superAltF4":lambda:(
            window.close(window.get_focused()), 
            subprocess.Popen(f"taskkill /f /im {window.get_focused()}",shell=True),
            subprocess.Popen(f"taskkill /f /im {window.get_focused()}.exe", shell=True)) if window.get_focused() else None,
    }
    
    for command, func in command_map.items():
        if isinstance(command, (str, tuple)):
            if isinstance(command, str) and message.startswith(command) or isinstance(command, tuple) and any(cmd in message for cmd in command):
                result = func(message) if 'message' in func.__code__.co_varnames else func()
                return result if result is not None else ""

        
        for commands in get_global_variable('all_func').values():
            for command, func in commands.items():
                if message.lstrip('/').startswith(command):
                    command_arguments = message[len(command)+1:].strip()
                    commandArgs = command_arguments.split("<|§|>")

                    if inspect.signature(func).parameters:
                        func(*commandArgs)
                    else:
                        func()
                    break
                        
    return jsonify({"success": True})

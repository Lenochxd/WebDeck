from app.utils.platform import is_win, is_linux

import json
import sys
import os
import subprocess
import time
import inspect
from flask import jsonify

if is_win: import win32gui
import pyperclip
if not is_linux or os.environ.get("DISPLAY"):
    import pyautogui
import keyboard

if is_win: from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
if is_win: import comtypes


from app.utils.logger import log
from app.utils.global_variables import get_global_variable

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



def handle_command(message=None):
    global all_func

    command_arguments = message
    message = message.replace("<|§|>", " ")

    if message == "/bypass-windows-firewall":
        fix_firewall_permission()

    if not message.strip().replace("\n", "").replace("\r", "") == "":
        log.info(f"Command received: {message}")
    if message.startswith("/debug-send"):
        data = {"message": "Hello, world!"}
        data = json.loads(message.replace("'", '"').replace("/debug-send", ""))
        # send(data)

    elif message.startswith("/exit"):
        sys.exit("/exit received")
        
    elif message.startswith("/usage"): # this is useless btw
        asked_device = []
        
        device = extract_asked_device(message)
        if device is not None:
            asked_device.append(device)
        
        log.debug(f"Asked device: {asked_device}")
        usage = get_usage(False, asked_device)
        log.debug(f"Usage data: {usage}")
        return jsonify(usage)

    elif message.startswith("/stop_sound"):
        return soundboard.stopsound()
    
    elif message.startswith(("/playsound ", "/playlocalsound ")):
        return soundboard.playsound(*soundboard.get_params(message))

    elif message.startswith("/locksession"):
        system.lock_session()

    elif message.startswith("/screensaversettings"):
        subprocess.Popen(
            "rundll32.exe desk.cpl,InstallScreenSaver toasters.scr", shell=True
        )

    elif message.startswith("/screensaver") and not message.startswith("/screensaversettings"):
        system.screensaver(message)

    elif message.startswith("/key"):
        key = message.replace("/key", "", 1).strip()
        pyautogui.press(key)

    elif message.startswith("/restartexplorer"):
        subprocess.Popen("taskkill /f /im explorer.exe", shell=True)
        time.sleep(0.5)
        subprocess.Popen("explorer.exe", shell=True)
        hwnd = window.get_by_name("explorer.exe")
        if hwnd:
            window.close(hwnd)

    elif message.startswith(("/kill", "/taskill", "/taskkill", "/forceclose")):
        system.kill(message)

    elif message.startswith("/restart"):
        system.restart_app(message)

    elif message.startswith("/clearclipboard"):
        system.clear_clipboard()

    elif message.startswith("/write "):
        keyboard.write(message.replace("/write ", ""))

    elif message.startswith("/writeandsend "):
        keyboard.write(message.replace("/writeandsend ", ""))
        keyboard.press("ENTER")


    elif message.startswith(("/appvolume +", "/appvolume -", "/appvolume set")):
        if not is_win:
            log.error("This command is only available on Windows")
            raise RuntimeError("This command is only available on Windows")
        
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
    
    elif message.startswith("/mediacontrol"):
        audio.media_control(message)

    elif message.startswith("/speechrecognition"):
        pyautogui.hotkey("win", "h")

    elif message.startswith("/superAltF4"):
        hwnd = window.get_focused()
        if hwnd:
            window.close(hwnd)
            subprocess.Popen(f"taskkill /f /im {hwnd}", shell=True)
            subprocess.Popen(f"taskkill /f /im {hwnd}.exe", shell=True)

    # FIXME: fix /firstplan
    elif message.startswith("/firstplan"):
        if not is_win:
            log.error("This command is only available on Windows")
            raise RuntimeError("This command is only available on Windows")
        
        window_name = message.replace("/firstplan", "").strip()

        hwnd = window.get_by_name(window_name)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            keyboard.press("ENTER")
            log.success(f"Window '{window_name}' has been brought to the foreground")
        else:
            log.error(f"Window '{window_name}' not found")
            raise RuntimeError(f"Window '{window_name}' not found")

    elif message.startswith("/setmicrophone"):
        audio.set_microphone_by_name(message.replace("/setmicrophone", "").strip())
        # PAS FINI
    elif message.startswith("/setoutputdevice"):
        audio.set_speakers_by_name(message.replace("/setoutputdevice", "").strip())
        # PAS FINI

    elif message.startswith("/copy"):
        if message.strip() == "/copy":
            pyautogui.hotkey("ctrl", "c")
        else:
            msg = message.replace("/copy ", "", 1)
            if msg.startswith("/copy"):
                msg = message.replace("/copy", "", 1)
            pyperclip.copy(msg)

    elif message.startswith("/paste"):
        if message.strip() == "/paste":
            pyautogui.hotkey("ctrl", "v")
        else:
            msg = message.replace("/paste ", "", 1)
            if msg.startswith("/paste"):
                msg = message.replace("/paste", "", 1)
            pyperclip.copy(msg)
            pyautogui.hotkey("ctrl", "v")

    elif message.startswith("/cut"):
        pyautogui.hotkey("ctrl", "x")

    elif message.startswith("/clipboard"):
        pyautogui.hotkey("win", "v")

    else:
        if message.startswith(("/volume", "/soundcontrol mute")):
            audio.change_volume(message)
            
        elif message.startswith("/spotify"):
            return spotify.handle_command(message)
            
        elif message.startswith("/obs"):
            return obs.handle_command(message)
        
        # /colorpicker lang:en type:text|name;text-original|name-original;hex;rgb;hsl copy:text;hex;rgb;hsl copy_type:raw|list displaytype:raw|list remove_hex_sharp:false
        elif message.startswith("/colorpicker"):
            color_picker.handle_command(message)
        
        elif message.startswith(("/openfolder", "/opendir",
                                "/openfile", "/start",
                                "/PC")):
            system.handle_command(message)
            
        elif message.startswith("/exec"):
            exec.python(message)

        elif message.startswith("/batch"):
            exec.batch(message)

        
        for commands in get_global_variable('all_func').values():
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

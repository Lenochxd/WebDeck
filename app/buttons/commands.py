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



def handle_command(message=None):
    global all_func

    command_arguments = message
    message = message.replace("<|§|>", " ")

    if message == "/bypass-windows-firewall":
        fix_firewall_permission()

    if not message.strip().replace("\n", "").replace("\r", "") == "":
        print("command recieved: " + message)
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
        
        print(asked_device)
        usage = get_usage(False, asked_device)
        print(usage)
        return jsonify(usage)

    elif message.startswith("/stop_sound"):
        return soundboard.stopsound()
    
    elif message.startswith(("/playsound ", "/playlocalsound ")):
        return soundboard.playsound(*soundboard.get_params(message))


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
            subprocess.Popen('"lib/nircmd.exe" monitor off', shell=True)
            kill_nircmd()

        elif message.endswith(("off", "false")):
            pyautogui.press("CTRL")

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
        window_name = (
            message.replace("/kill", "")
            .replace("/taskill", "")
            .replace("/taskkill", "")
            .replace("/forceclose", "")
        )
        hwnd = window.get_by_name(window_name)
        if hwnd:
            print(f"Window '{window_name}' found with handle : {hwnd}")
        else:
            print(f"Window '{window_name}' not found")
        try:
            window.close(hwnd)
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
        keyboard.write(message.replace("/write ", ""))

    elif message.startswith("/writeandsend "):
        keyboard.write(message.replace("/writeandsend ", ""))
        keyboard.press("ENTER")


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
        pyautogui.press("volumemute")
    elif message.startswith("/mediacontrol playpause"):
        pyautogui.press("playpause")
    elif message.startswith("/mediacontrol previous"):
        pyautogui.press("prevtrack")
    elif message.startswith("/mediacontrol next"):
        pyautogui.press("nexttrack")

    elif message.startswith("/speechrecognition"):
        pyautogui.hotkey("win", "h")

    elif message.startswith("/superAltF4"):
        hwnd = window.get_focused()
        if hwnd:
            window.close(hwnd)
            subprocess.Popen(f"taskkill /f /im {hwnd}", shell=True)
            subprocess.Popen(f"taskkill /f /im {hwnd}.exe", shell=True)

    # TODO: fix /firstplan
    elif message.startswith("/firstplan"):
        window_name = message.replace("/firstplan", "").strip()

        hwnd = window.get_by_name(window_name)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            keyboard.press("ENTER")
            print(f"Window '{window_name}' brought to the foreground")
        else:
            print(f"Window '{window_name}' not found")

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
        if message.startswith("/volume"):
            audio.change_volume(message)
            
        elif message.startswith("/spotify"):
            spotify.handle_command(message)
            
        elif message.startswith("/obs"):
            obs.handle_command(message)
        
        # /colorpicker lang:en type:text|name;text-original|name-original;hex;rgb;hsl copy:text;hex;rgb;hsl copy_type:raw|list displaytype:raw|list remove_hex_sharp:false
        elif message.startswith("/colorpicker"):
            color_picker.handle_command(message)
        
        elif message.startswith(("/openfolder", "/opendir",
                                "/openfile", "/start")):
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

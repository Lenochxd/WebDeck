import json
import os
import sys
import subprocess
import threading
import time
import numpy as np
import inspect
from flask import jsonify

import win32gui
if sys.platform == 'win32':
    from win10toast import ToastNotifier
import pyperclip
import pyautogui
import keyboard
import mss
from obswebsocket import obsws, events
from obswebsocket import requests as obsrequests
from PIL import Image # color picker

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import comtypes


from app.functions.global_variables import get_global_variable
from app.functions.translate import translate
from app.functions.kill_nircmd import kill_nircmd

from app.functions.firewall import fix_firewall_permission
from app.buttons.usage import extract_asked_device, get_usage
from app.buttons.color_picker import getarg, get_color_name
from app.buttons.audio import *
import app.buttons.exec as exec
import app.buttons.window as window
import app.buttons.soundboard as soundboard
import app.buttons.spotify as spotify
import app.buttons.obs as obs


threads = []
if sys.platform == 'win32':
    toaster = ToastNotifier()


def command(message=None):
    global all_func
    
    text = get_global_variable("text")

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
    
    elif message.startswith("/playsound ") or message.startswith("/playlocalsound "):
        return soundboard.playsound(*soundboard.get_params(message))

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
                
                threads.append(threading.Thread(target=exec.execute_python_file, args=(python_file,), daemon=True))
                threads[-1].start()
        elif "type:file_path" in message:
            python_file = message.replace("/exec ", "").replace("type:file_path", "").strip()
            
            threads.append(threading.Thread(target=exec.execute_python_file, args=(python_file,), daemon=True))
            threads[-1].start()
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

        if ":" in path:
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
        pyautogui.press("volumemute")
    elif message.startswith("/mediacontrol playpause"):
        pyautogui.press("playpause")
    elif message.startswith("/mediacontrol previous"):
        pyautogui.press("prevtrack")
    elif message.startswith("/mediacontrol next"):
        pyautogui.press("nexttrack")

    elif message.startswith("/speechrecognition"):
        pyautogui.hotkey("win", "h")

    # /colorpicker lang:en type:text|name;text-original|name-original;hex;rgb;hsl copy:text;hex;rgb;hsl copytype:raw|list showtype:raw|list remove_hex_sharp:false
    elif message.startswith("/colorpicker"):

        x, y = pyautogui.position()

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
            named_original = get_color_name(hex_color, colorsjson)
            named_color = named_original
        else:
            named_original = get_color_name(hex_color, colorsjson)
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

        if sys.platform == 'win32':
            toaster.show_toast(
                title, message, icon_path=icon, duration=duration, threaded=True
            )

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
        set_microphone_by_name(message.replace("/setmicrophone", "").strip())
        # PAS FINI
    elif message.startswith("/setoutputdevice"):
        set_speakers_by_name(message.replace("/setoutputdevice", "").strip())
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
        if message.startswith("/spotify"):
            spotify.handle_command(message, text)
            
        if message.startswith("/obs"):
            obs.handle_command(message, text)
            
        
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

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
import pyautogui as keyboard
import keyboard as keyboard2
import mss
import vlc
from obswebsocket import obsws, events
from obswebsocket import requests as obsrequests
import spotipy
from PIL import Image # color picker

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import comtypes


from app.functions.global_variables import get_global_variable
from app.functions.show_error import show_error
from app.functions.translate import translate

from app.functions.firewall import fix_firewall_permission
from app.buttons.usage import extract_asked_device, get_usage
from app.buttons.color_picker import getarg, get_color_name
from app.buttons.audio import *
import app.buttons.kill_nircmd as kill_nircmd
import app.buttons.exec as exec
import app.buttons.window as window
import app.buttons.soundboard as soundboard
import app.buttons.spotify as spotify


threads = []
spotify_token = spotify.initialize()
if sys.platform == 'win32':
    toaster = ToastNotifier()


def command(message=None):
    global all_func, obs, obs_host, obs_port, obs_password, obs
    
    config = get_global_variable("config")
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
            keyboard.press("CTRL")

    elif message.startswith("/key"):
        key = message.replace("/key", "", 1).strip()
        keyboard.press(key)

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
        # TODO: Follow the specified artist
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

        obs.disconnect()
        
    else:
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

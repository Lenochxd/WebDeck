from app.utils.platform import is_linux

import os
import keyboard
if not is_linux or os.environ.get("DISPLAY"):
    import pyautogui


def handle_command(message):
    
    if message.startswith("/mediacontrol playpause"):
        playpause()
    elif message.startswith("/mediacontrol previous"):
        prevtrack()
    elif message.startswith("/mediacontrol next"):
        nexttrack()


def playpause():
    try:
        if is_linux:
            keyboard.send("play/pause media")
        else:
            pyautogui.press("playpause")
    except:
        if is_linux:
            keyboard.send(164)
        else:
            keyboard.send(-179)

def prevtrack():
    try:
        if is_linux:
            keyboard.send("previous track")
        else:
            pyautogui.press("prevtrack")
    except:
        if is_linux:
            keyboard.send(165)
        else:
            keyboard.send(-177)

def nexttrack():
    try:
        if is_linux:
            keyboard.send("next track")
        else:
            pyautogui.press("nexttrack")
    except:
        if is_linux:
            keyboard.send(163)
        else:
            keyboard.send(-176)
from app.utils.platform import is_linux

import os
if not is_linux or os.environ.get("DISPLAY"):
    import pyautogui
    from pynput.keyboard import Controller, Key
    keyboard = Controller()


def handle_command(message):
    
    if message.startswith("/mediacontrol playpause"):
        playpause()
    elif message.startswith("/mediacontrol previous"):
        prevtrack()
    elif message.startswith("/mediacontrol next"):
        nexttrack()


def playpause():
    try:
        keyboard.tap(Key.media_play_pause)
    except Exception:
        pyautogui.press("playpause")

def prevtrack():
    try:
        keyboard.tap(Key.media_previous)
    except Exception:
        pyautogui.press("prevtrack")

def nexttrack():
    try:
        keyboard.tap(Key.media_next)
    except Exception:
        pyautogui.press("nexttrack")

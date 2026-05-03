from app.utils.platform import is_linux

import os
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
    pyautogui.press("playpause")

def prevtrack():
    pyautogui.press("prevtrack")

def nexttrack():
    pyautogui.press("nexttrack")

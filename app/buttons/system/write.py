from app.utils.platform import is_windows

import keyboard
import pyautogui
from pynput.keyboard import Controller
pynput = Controller()


def write(text):
    if is_windows:
        keyboard.write(text)
    else:
        pynput.type(text)


def handle_command(message):
    text = message.replace("/writeandsend", "",1).replace("/write", "", 1).strip()
    
    if message.startswith("/writeandsend "):
        write(text)
        pyautogui.press("enter")
    
    if message.startswith("/write "):
        write(text)

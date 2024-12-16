from app.utils.platform import is_windows, is_linux

import os
import subprocess
import pyautogui
from app.utils.logger import log
from .. import window

def kill(message):
    process = (
        message.replace("/kill", "")
        .replace("/taskill", "")
        .replace("/taskkill", "")
        .replace("/forceclose", "")
    ).strip()
    
    if is_windows:
        if process.endswith(".exe"):
            subprocess.Popen(f"taskkill /f /im {process}", shell=True)
        else:
            window_name = process
            hwnd = window.get_by_name(window_name)
            if hwnd:
                log.debug(f"Window '{window_name}' found with handle : {hwnd}")
                try:
                    window.close(hwnd)
                except:
                    subprocess.Popen(f"taskkill /f /im {window_name}.exe", shell=True)
            else:
                log.debug(f"Window '{window_name}' not found")
                subprocess.Popen(f"taskkill /f /im {window_name}.exe", shell=True)
    
    elif is_linux:
        log.debug(f"Killing process '{process}'")
        if subprocess.run(f"killall --ignore-case {process}", shell=True).returncode == 0:
            log.success(f"Process '{process}' killed successfully")
        else:
            log.error(f"Process '{process}' not found")
            raise RuntimeError(f"Process '{process}' not found")
    
    else:
        raise NotImplementedError("Screensaver is not implemented for this platform.")


def screensaver_off():
    pyautogui.press("CTRL")
    if is_linux:
        os.system("gnome-screensaver-command -d")
    
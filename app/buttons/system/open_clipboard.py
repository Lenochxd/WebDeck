from app.utils.platform import is_windows, is_linux

import os
import subprocess
if not is_linux or os.environ.get("DISPLAY"):
    import pyautogui
    
from app.utils.get_process_path import get_process_path
from app.utils.logger import log


def open_clipboard():
    if is_windows:
        pyautogui.hotkey("win", "v")
    
    if is_linux:
        def is_command_available(command):
            """Check if a command is available on the system."""
            try:
                if subprocess.run(["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                    return True
                return False
            except FileNotFoundError:
                return False

        # Check for common clipboard managers and open them if installed
        clipboard_managers = {
            "copyq": f"{get_process_path('copyq')} show",
            "gpaste-client": f"{get_process_path('gpaste-client')} ui",
            "clipman": f"{get_process_path('clipman')} show-history",
            "parcellite": f"{get_process_path('parcellite')}",
            "xfce4-clipman": f"{get_process_path('xfce4-clipman-history')}",
            "klipper": f"{get_process_path('qdbus')} org.kde.klipper /klipper org.kde.klipper.klipper.showHistory",
            "diodon": f"{get_process_path('diodon')} --indicator",
        }

        for manager, command in clipboard_managers.items():
            if is_command_available(manager):
                if subprocess.run(command, shell=True).returncode == 0:
                    log.success(f"Opened clipboard manager: '{manager}' Using command: '{command}'")
                else:
                    log.error(f"Failed to open {manager}")
                
                return
        
        pyautogui.hotkey("win", "v")
        
        log.error("No supported clipboard manager found. Please install one, e.g., 'copyq'. Performing default action (Win+V).")
        raise RuntimeError("No supported clipboard manager found. Please install one, e.g., 'copyq'.  Performing default action (Win+V).")
    
    else:
        raise NotImplementedError("This is not implemented for this platform.")

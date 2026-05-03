from app.utils.platform import is_windows, is_linux

import subprocess
from app.utils.get_process_path import get_process_path, xclip
from app.utils.logger import log


def clear_clipboard():
    if is_windows:
        subprocess.Popen('cmd /c "echo off | clip"', shell=True)
        log.success("Clipboard cleared")
    
    elif is_linux:
        # Method 1: Using xclip
        if xclip and subprocess.run(f"echo -n | {xclip} -selection clipboard", shell=True).returncode == 0:
            log.success("Clipboard cleared using xclip")
            return
        # Method 2: Using xsel
        xsel = get_process_path('xsel')
        if xsel and subprocess.run(f"{xsel} --clipboard --clear", shell=True).returncode == 0:
            log.success("Clipboard cleared using xsel")
            return
        
        # Method 3: Using wl-copy (for Wayland)
        wl_copy = get_process_path('wl-copy')
        if wl_copy and subprocess.run(f"echo -n | {wl_copy}", shell=True).returncode == 0:
            log.success("Clipboard cleared using wl-copy")
            return
        
        else:
            log.error("Failed to clear the clipboard")
            raise RuntimeError(
                "Failed to clear the clipboard, no clipboard manager found. Please install xclip, xsel or wl-clipboard."
            )
    
    else:
        raise NotImplementedError("Clearing the clipboard is not implemented for this platform.")

from app.utils.platform import is_windows, is_linux

import subprocess
from app.utils.logger import log


def clear_clipboard():
    if is_windows:
        subprocess.Popen('cmd /c "echo off | clip"', shell=True)
        log.success("Clipboard cleared")
    
    elif is_linux:
        # Method 1: Using xclip
        if subprocess.run("echo -n | xclip -selection clipboard", shell=True).returncode == 0:
            log.success("Clipboard cleared using xclip")
            return
        # Method 2: Using xsel
        elif subprocess.run("xsel --clipboard --clear", shell=True).returncode == 0:
            log.success("Clipboard cleared using xsel")
            return
        
        # Method 3: Using wl-copy (for Wayland)
        elif subprocess.run("echo -n | wl-copy", shell=True).returncode == 0:
            log.success("Clipboard cleared using wl-copy")
            return
        
        else:
            log.error("Failed to clear the clipboard")
            raise RuntimeError(
                "Failed to clear the clipboard, no clipboard manager found. Please install xclip, xsel or wl-clipboard."
            )
    
    else:
        raise NotImplementedError("Clearing the clipboard is not implemented for this platform.")
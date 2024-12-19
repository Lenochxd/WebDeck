from app.utils.platform import is_windows, is_linux

import os
import subprocess
if not is_linux or os.environ.get("DISPLAY"):
    import pyautogui
from app.utils.kill_nircmd import kill_nircmd
from app.utils.logger import log


def handle_command(message):
    if message.endswith(("on", "/screensaver", "start")):
        screensaver()

    elif message.endswith(("hard", "full", "black")):
        screensaver(hard=True)

    elif message.endswith(("off", "false")):
        screensaver_off()
    
    else:
        return False
    return True
    
    
def screensaver(hard=False):
    if is_windows:
        if hard:
            subprocess.Popen('"lib/nircmd.exe" monitor off', shell=True)
            kill_nircmd()
        else:
            subprocess.Popen("%windir%/system32/scrnsave.scr /s", shell=True)
    
    elif is_linux:
        # Try X11 (xset), then Wayland (gnome-screensaver)
        if subprocess.run("xset dpms force off", shell=True).returncode == 0:
            pass
        elif subprocess.run("gnome-screensaver-command -a", shell=True).returncode == 0:
            pass
        elif subprocess.run("swaymsg 'output * dpms off'", shell=True).returncode == 0:
            pass
        else:
            log.error("Unable to enable screensaver.")
            raise RuntimeError("Unable to enable screensaver.")
    
    else:
        raise NotImplementedError("Screensaver is not implemented for this platform.")


def screensaver_off():
    pyautogui.press("CTRL")
    if is_linux:
        os.system("gnome-screensaver-command -d")
    
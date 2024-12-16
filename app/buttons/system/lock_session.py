from app.utils.platform import is_windows, is_linux, is_mac

import subprocess
from app.utils.logger import log


def lock_session():
    """Lock the user's session."""
    if is_windows:
        # Lock workstation on Windows
        subprocess.Popen("Rundll32.exe user32.dll,LockWorkStation", shell=True)
        
    elif is_linux:
        # Try various Linux locking methods
        if subprocess.run("dm-tool lock", shell=True).returncode == 0:
            return
        elif subprocess.run("xdg-screensaver lock", shell=True).returncode == 0:
            return
        elif subprocess.run("gnome-screensaver-command -l", shell=True).returncode == 0:
            return
        elif subprocess.run("loginctl lock-session", shell=True).returncode == 0:
            return
        elif subprocess.run("swaylock", shell=True).returncode == 0:
            return
        else:
            log.error("Unable to lock the session.")
            raise RuntimeError("Unable to lock the session.")

    else:
        raise NotImplementedError("Screensaver is not implemented for this platform.")

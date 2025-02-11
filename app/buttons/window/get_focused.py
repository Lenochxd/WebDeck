from app.utils.platform import is_windows, is_linux, is_wayland

if is_windows: import win32gui
if not is_wayland:
    from app.utils.get_process_path import xdotool
from app.utils.logger import log
import subprocess


def get_focused_window():
    if is_windows:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd == 0:
            log.debug("No window has focus")
            return None
        else:
            window_title = win32gui.GetWindowText(hwnd)
            log.debug(f"Focused window: {window_title}")
            return window_title
    
    elif is_linux:
        try:
            window_id = subprocess.check_output([xdotool, "getwindowfocus"], universal_newlines=True).strip()
            window_title = subprocess.check_output([xdotool, "getwindowname", window_id], universal_newlines=True).strip()
            log.debug(f"Focused window: '{window_title}' ; window_id: '{window_id}'")
            return window_id
        except subprocess.CalledProcessError:
            log.debug("No window has focus")
            return None
        
    else:
        log.error("This command is not implemented for this platform.")
        raise RuntimeError("This command is not implemented for this platform.")

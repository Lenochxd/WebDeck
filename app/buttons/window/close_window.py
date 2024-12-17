from app.utils.platform import is_windows, is_linux

import subprocess
if is_windows:
    import win32gui
    import win32con
from app.utils.logger import log


def close_window(window):
    if is_windows:
        # Find the window
        window_name = window
        hwnd = win32gui.FindWindow(None, window_name)
        if hwnd == 0:
            log.warning(f"Window with title '{window_name}' not found or already closed")
            raise RuntimeError(f"Window with title '{window_name}' not found or already closed")
        
        # Close the window
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    
    elif is_linux:
        # While using Linux, the window name is the window ID
        window_id = window
        if subprocess.run(["xdotool", "windowclose", window_id]).returncode != 0:
            log.warning(f"Window with ID '{window_id}' not found or already closed")
            raise RuntimeError(f"Window with ID '{window_id}' not found or already closed")
        log.success(f"Window with ID '{window_id}' has been closed")
    
    else:
        log.error("This command is not implemented for this platform.")
        raise RuntimeError("This command is not implemented for this platform.")

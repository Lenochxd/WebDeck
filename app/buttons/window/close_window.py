import win32gui
import win32con
from app.utils.logger import log


def close_window(window_title):
    # Find the window
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        log.warning(f"Window with title '{window_title}' not found or already closed")
        raise RuntimeError(f"Window with title '{window_title}' not found or already closed")
    
    # Close the window
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
from app.utils.platform import is_win

if is_win:
    import win32gui
    import win32con
from app.utils.logger import log


def bring_window_to_front(window_title):
    if not is_win:
        log.error("This command is only available on Windows")
        raise RuntimeError("This command is only available on Windows")
    
    # Find the window
    hwnd = win32gui.FindWindow(None, str(window_title))
    if hwnd == 0:
        log.error(f"Window with title '{window_title}' not found")
        raise Exception(f"Window with title '{window_title}' not found")
    
    # Bring the window to the foreground
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
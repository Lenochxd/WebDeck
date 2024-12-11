from app.utils.platform import is_win

if is_win: import win32gui
from app.utils.logger import log


def get_focused_window():
    if not is_win:
        log.error("This command is only available on Windows")
        raise RuntimeError("This command is only available on Windows")
    
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        log.debug("No window has focus")
        return None
    else:
        window_title = win32gui.GetWindowText(hwnd)
        log.debug(f"Focused window: {window_title}")
        return window_title
import win32gui
from app.utils.logger import log


def get_focused_window():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        log.debug("No window has focus")
        return None
    else:
        window_title = win32gui.GetWindowText(hwnd)
        log.debug(f"Focused window: {window_title}")
        return window_title
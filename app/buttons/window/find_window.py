import win32gui
import win32con


# Find a window with a specific title
def find_window_with_name(hwnd, name):
    window_name = win32gui.GetWindowText(hwnd)
    if name.lower().replace(".exe", "") in window_name.lower().replace(".exe", ""):
        return hwnd
    return None

# Function to get the window corresponding to a given name
def get_window_by_name(name):
    hwnd = win32gui.FindWindow(None, None)
    window_hwnd = None
    while hwnd != 0:
        if find_window_with_name(hwnd, name) is not None:
            window_hwnd = hwnd
            break
        hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
    return window_hwnd
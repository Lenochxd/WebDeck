import win32gui


def get_focused_window():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        print("No window has focus")
        return None
    else:
        window_title = win32gui.GetWindowText(hwnd)
        print(f"Focused window: {window_title}")
        return window_title
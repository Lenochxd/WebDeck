import win32gui
import win32con


def close_window(window_title):
    # Find the window
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print("Window not found")
        return
    
    # Close the window
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
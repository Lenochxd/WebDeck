import ctypes

def show_error(message):
    print(message)
    ctypes.windll.user32.MessageBoxW(None, message, "WebDeck Error", 0)
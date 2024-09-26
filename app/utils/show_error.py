import ctypes

def show_error(message, title="WebDeck Error"):
    print(message)
    ctypes.windll.user32.MessageBoxW(None, message, title, 0)
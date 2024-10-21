import ctypes
import traceback
import tkinter as tk
from tkinter import messagebox


def show_error(message=None, title="WebDeck Error", error=True, exception=None) -> None:
    if exception is not None:
        if message is not None:
            message = f"{message}\n\n\n{str(exception)}\n\n{traceback.format_exc()}"
        else:
            message = f"{str(exception)}\n\n{traceback.format_exc()}"
    
    if error:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    else:
        ctypes.windll.user32.MessageBoxW(None, message, title, 0)
    
    print(message)

import pyperclip
import webbrowser
import ctypes
import traceback
import tkinter as tk
from tkinter import messagebox
from .languages import text
from .logger import log


def show_error(message=None, title="WebDeck Error", error=True, exception=None) -> None:
    if exception is not None:
        log.exception(exception, message, expected=False)
        if message is not None:
            message = f"{message}\n\n\n{str(exception)}\n\n{traceback.format_exc()}"
        else:
            message = f"{str(exception)}\n\n{traceback.format_exc()}"
    else:
        log.error(message)
    
    if error:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        
        if messagebox.askyesno(
            text("open_github_issue_prompt_title"),
            text("open_github_issue_prompt_message")
        ):
            issue_title = f"[AUTO] {title} - {str(exception)}".replace(" ", "%20")
            issue_body = (
                "**Describe the bug**     <!-- (edit this) -->\n"
                "A clear and concise description of what the bug is.\n\n"
                "**Steps to reproduce**     <!-- (example) -->\n"
                "1. Go to '...'\n"
                "2. Click on '....'\n"
                "3. Scroll down to '....\n\n\n"
                "## The error\n"
                f"{message}"
            )
            issue_body = issue_body.replace("\n", "%0A").replace(" ", "%20").replace("#", "%23")
            webbrowser.open(f"https://github.com/Lenochxd/WebDeck/issues/new?labels=bug&template=bug_report.md&title={issue_title}&body={issue_body}")
        elif messagebox.askyesno(
            text("copy_to_clipboard_prompt_title"),
            text("copy_to_clipboard_prompt_message")
        ):
            pyperclip.copy(message)
        
        root.destroy()
    else:
        ctypes.windll.user32.MessageBoxW(None, message, title, 0)
        

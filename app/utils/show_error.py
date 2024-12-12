import pyperclip
import webbrowser
import ctypes
import traceback
import tkinter as tk
from tkinter import messagebox
from .languages import text
from .logger import log


def _show_error(message=None, title="WebDeck Error", error=True, exception=None) -> None:
    if exception is not None:
        log.exception(exception, message, expected=False)
        if message is not None:
            github_message = f"`{message}`\n\n\n```\n{str(exception)}\n```\n\n```{traceback.format_exc()}```"
            message = f"{message}\n\n\n{str(exception)}\n\n{traceback.format_exc()}"
        else:
            github_message = f"```\n{str(exception)}\n```\n\n```{traceback.format_exc()}```"
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
                f"{github_message}"
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
        
def show_error(message=None, title="WebDeck Error", error=True, exception=None) -> None:
    """
    Displays an error message using a message box and optionally logs the error and opens a GitHub issue.
    Args:
        message (str, optional): The error message to display. Defaults to None.
        title (str, optional): The title of the error message box. Defaults to "WebDeck Error".
        error (bool, optional): Display the error message box using tkinter instead of windll.user32.messageBoxW. Defaults to True.
        exception (Exception, optional): The exception to log and include in the message. Defaults to None.
    Returns:
        None
    """
    try:
        _show_error(message, title, error, exception)
    except Exception as e:
        log.exception(
            e,
            message="An error occurred while trying to display an error message.\nError message: {message}\nTitle: {title}\nError: {error}",
            expected=True,
            print_log=False
        )

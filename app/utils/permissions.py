import os
import sys
import ctypes

def is_root():
    # Checks the effective UID
    return os.geteuid() == 0

is_sudo = is_root

def is_admin():
    if sys.platform == "win32":
        return ctypes.windll.shell32.IsUserAnAdmin()
    else:
        return is_root()

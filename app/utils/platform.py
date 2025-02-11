import os
import sys

def platform(lower=False):
    """
    Determines the current operating system platform.
    Args:
        lower (bool): If True, returns the platform name in lowercase. Defaults to False.
    Returns:
        str: The name of the current operating system platform. Possible values are 'Linux', 'Windows', 'macOS', or 'Unknown'.
    """
    if lower:
        return platform().lower()
    
    if sys.platform.startswith('linux'):
        return 'Linux'
    elif sys.platform.startswith('win'):
        return 'Windows'
    elif sys.platform.startswith('darwin'):
        return 'macOS'
    else:
        return 'Unknown'


def is_windows():
    return platform() == 'Windows'

def is_linux():
    return platform() == 'Linux'

def is_macos():
    return platform() == 'macOS'

def is_wayland():
    return os.environ.get("XDG_SESSION_TYPE") == "wayland"


is_windows = is_windows()
is_win = is_windows

is_linux = is_linux()
is_wayland = is_wayland()

is_macos = is_macos()
is_mac = is_macos
import os
import sys
from .platform import is_linux


def locate_file_directory(filename, base_dir=None) -> str:
    """
    Helper function to locate a file in the current directory or up to 4 parent directories.
    This is necessary because the base path can be 'WebDeck/lib/library.zip/app/utils' for example.
    If the application is not frozen, returns the current directory directly.
    """
    if not getattr(sys, 'frozen', False):
        return os.getcwd()

    search_dirs = [base_dir or os.getcwd(), os.path.abspath(os.path.dirname(__file__))]

    for search_dir in search_dirs:
        current_dir = search_dir
        for _ in range(5):  # Check current directory and up to 4 parent directories
            if os.path.exists(os.path.join(current_dir, filename)):
                return current_dir
            current_dir = os.path.dirname(current_dir)

    raise FileNotFoundError(f"{filename} not found in the current directory.")


def get_base_dir() -> str:
    """
    Returns the base project directory by navigating up to 2 levels to find 'WebDeck.exe' on Windows
    or 'webdeck' binary on Linux. If the application is not frozen, returns the current directory directly.
    """
    if is_linux and getattr(sys, 'frozen', False):
        return locate_file_directory("webdeck")
    return locate_file_directory("WebDeck.exe")

def get_update_dir() -> str:
    """
    Returns the directory containing 'update/update.exe' by priority, then 'update.exe' on Windows
    or 'webdeck-update' binary on Linux by navigating up to 2 levels. If the application is not frozen, returns the current directory directly.
    """
    base_dir = os.path.join(get_base_dir(), "update")
    if is_linux and getattr(sys, 'frozen', False):
        return locate_file_directory("webdeck-update", base_dir)
    return locate_file_directory("update.exe", base_dir)


def chdir_base() -> None:
    """
    Changes the current working directory to the base project directory.
    """
    os.chdir(get_base_dir())

def chdir_update() -> None:
    """
    Changes the current working directory to the update directory.
    """
    os.chdir(get_update_dir())


if __name__ == '__main__':
    print(get_base_dir())
    print(get_update_dir())
    chdir_base()
    print(os.getcwd())
    chdir_update()
    print(os.getcwd())
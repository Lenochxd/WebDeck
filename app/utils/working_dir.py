import os
import sys


def locate_file_directory(filename, base_dir=None) -> str:
    """
    Helper function to locate a file in the current directory or up to 2 parent directories.
    If the application is not frozen, returns the current directory directly.
    """
    if not getattr(sys, 'frozen', False):
        return os.getcwd()
    
    current_dir = base_dir or os.getcwd()
    for _ in range(3):  # Check current directory and up to 2 parent directories
        if os.path.exists(os.path.join(current_dir, filename)):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    raise FileNotFoundError(f"{filename} not found in the current directory or up to 2 parent directories.")


def get_base_dir() -> str:
    """
    Returns the base project directory by navigating up to 2 levels to find 'WebDeck.exe'.
    If the application is not frozen, returns the current directory directly.
    """
    return locate_file_directory("WebDeck.exe")

def get_update_dir() -> str:
    """
    Returns the directory containing 'update/update.exe' by priority, then 'update.exe' by navigating up to 2 levels.
    If the application is not frozen, returns the current directory directly.
    """
    base_dir = os.path.join(get_base_dir(), "update")
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
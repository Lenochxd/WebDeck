from app.utils.platform import is_windows, is_linux, is_mac
import os


def openfile(path):
    def open_path(path):
        if is_windows:
            os.startfile(path)
        elif is_linux:
            os.system(f'xdg-open "{path}"')
        elif is_mac:
            os.system(f'open "{path}"')
    
    if "://" not in path and ":" in path:
        initial_path = os.getcwd()
        file_directory = os.path.dirname(path)
        try:
            os.chdir(file_directory)
            open_path(path)
        finally:
            os.chdir(initial_path)
    else:
        open_path(path)
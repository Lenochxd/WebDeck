import os


def openfile(path):
    if ":" in path:
        initial_path = os.getcwd()
        try:
            file_directory = os.path.dirname(path)
            os.chdir(file_directory)
            os.startfile(path)
        finally:
            os.chdir(initial_path)
    else:
        os.startfile(path)
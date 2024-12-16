import os
from app.utils.platform import is_windows, is_linux, is_mac
from app.utils.logger import log


def opendir(message):
    def normalize_path(path):
        return path.replace('\\\\', '\\').replace('\\', '/')

    path = message.replace("/openfolder", "", 1).replace("/opendir", "", 1).strip()
    path = normalize_path(path)

    path = os.path.abspath(path)
    log.debug(f"Opening directory: {path}")

    if is_windows:
        os.system(f'explorer "{path}"')
    elif is_linux:
        os.system(f'xdg-open "{path}"')
    elif is_mac:
        os.system(f'open "{path}"')

    return path
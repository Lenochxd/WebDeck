import os
from subprocess import Popen
from app.utils.logger import log


def opendir(message):
    def normalize_path(path):
        return path.replace('\\\\', '\\').replace('\\', '/')

    path = message.replace("/openfolder", "", 1).replace("/opendir", "", 1).strip()
    path = normalize_path(path)

    path = os.path.abspath(path)
    log.debug(f"Opening directory: {path}")
    Popen(f'explorer "{path}"')

    return path
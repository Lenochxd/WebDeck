from .openfile import openfile
from .opendir import opendir


def handle_command(message):
    if message.startswith(("/openfolder", "/opendir")):
        opendir(message)
        
    elif message.startswith(("/openfile", "/start")):
        path = message.replace("/openfile", "", 1).replace("/start", "", 1).strip()
        openfile(path)
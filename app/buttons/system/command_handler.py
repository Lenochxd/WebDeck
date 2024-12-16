from .openfile import openfile
from .opendir import opendir
from . import power


def handle_command(message):
    if message.startswith(("/openfolder", "/opendir")):
        opendir(message)
        
    elif message.startswith(("/openfile", "/start")):
        path = message.replace("/openfile", "", 1).replace("/start", "", 1).strip()
        openfile(path)
    
    elif message.startswith("/PCshutdown"):
        power.shutdown()

    elif message.startswith("/PCrestart"):
        power.restart()
        
    elif message.startswith("/PCsleep"):
        power.sleep()

    elif message.startswith("/PChibernate"):
        power.hibernate()
        
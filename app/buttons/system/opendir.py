import os
import sys
from subprocess import Popen
from app.utils.logger import log


def opendir(message):
    # FIXME: works weirdly
    
    path = message.replace("/openfolder", "", 1).replace("/opendir", "", 1).strip()
    pathtemp = path.replace('\\\\','\\').replace('\\', '/')
    
    if not ":" in pathtemp:
        path = os.path.join(os.getcwd(), path)
        if not os.path.isdir(path):
            path = os.path.join(os.path.dirname(sys.executable), path)
            if not os.path.isdir(path):
                path = pathtemp
    else:
        path = pathtemp
        
    path = path.replace('\\\\','\\').replace('\\', '/')
    
    # if not path.endswith('/'):
    #     path += '/'
        
    if not os.path.isdir(path):
        if path.startswith('/'):
            path = path[1:]
        path = f"C:/.Code/WebDeck/{path}"
    
    path = path.replace('/', '\\')
    log.debug(f"Opening directory: {path}")
    Popen(f'explorer "{path}"')
    # os.startfile(path)
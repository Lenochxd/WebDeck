import ctypes
import sys
import os.path
import threading

from app.utils.settings.get_config import get_config

settings = get_config()['settings']

if settings['app_admin']:
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

from app.utils.show_error import show_error
from app.utils.is_opened import is_opened
import app.utils.languages as languages
from app.utils.logger import log


def run_server_thread():
    from app.server import run_server
    try:
        run_server()
    except Exception as e:
        show_error(exception=e)

def initialize_tray_icon():
    from app.tray import create_tray_icon
    try:
        create_tray_icon()
    except Exception as e:
        if os.name == 'nt':
            show_error(exception=e)
        else:
            log.exception(e, "Failed to initialize tray icon", expected=False)


if not is_opened():
    log.info("Starting WebDeck")
    
    log.info("Loading translations")
    languages.init(
        lang_files_directory="webdeck/translations",
        misc_lang_files_directory="webdeck/translations/misc",
        default_language=settings['language']
    )
    
    log.info("Starting server thread")
    server_thread = threading.Thread(target=run_server_thread, daemon=True)
    server_thread.start()
    
    log.info("Initializing tray icon")
    initialize_tray_icon()
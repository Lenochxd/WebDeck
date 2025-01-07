import ctypes
import sys
import os
import threading

from app.utils.logger import log
from app.utils.settings.get_config import get_config
from app.utils.args import parse_args, get_arg
from app.utils.working_dir import chdir_base
from app.utils.permissions import is_admin
from app.utils.platform import is_windows, is_linux


def attach_console():
    if not getattr(sys, "frozen", False):
        return
    
    try:
        # Attach to an existing console
        ctypes.windll.kernel32.AttachConsole(-1)
        
        # Redirect standard output and error to the console
        sys.stdout = open("CONOUT$", "w")
        sys.stderr = open("CONOUT$", "w")
        
        print()
    except Exception as e:
        print(f"Error attaching console: {e}")

attach_console()
chdir_base()

parse_args()

config = get_config(check_updates=True, save_updated_config=True)
settings = config['settings']

if settings['app_admin'] and not get_arg('no_admin'):
    if not is_admin():
        if is_windows:
            # Rebuild the command including all arguments
            params = " ".join([__file__] + sys.argv[1:])
            # Restart the program with admin privileges and include arguments
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            sys.exit()
        
        else:
            # No need to run as admin on Linux
            pass

from app.utils.welcome_popup import show_popup
from app.utils.show_error import show_error
from app.utils.is_opened import is_opened
import app.utils.languages as languages


def run_server_thread():
    from app.server import run_server
    try:
        run_server()
    except Exception as e:
        show_error(exception=e)

def initialize_tray_icon():
    from app.tray import create_tray_icon
    try:
        if is_linux and not os.environ.get('DISPLAY'):
            log.warning("No display available. Skipping tray icon initialization.")
            return False
        create_tray_icon()
    except Exception as e:
        show_error(message="Failed to initialize tray icon", exception=e)

if not is_opened() or get_arg('force_start'):
    log.info("Starting WebDeck")
    
    # Check if a display is available on Linux
    if is_linux and not os.environ.get('DISPLAY'):
        log.debug(f"DISPLAY: {os.environ.get('DISPLAY')}")
        log.warning("No display available. Please run WebDeck on a graphical environment.")
    
    log.info("Loading translations")
    languages.init(
        lang_files_directory="webdeck/translations",
        misc_lang_files_directory="webdeck/translations/misc",
        default_language=settings['language']
    )
    
    log.info("Starting server thread")
    server_thread = threading.Thread(target=run_server_thread, daemon=True)
    server_thread.start()
    
    log.info("Starting welcome popup thread")
    popup_thread = threading.Thread(target=show_popup, daemon=True)
    popup_thread.start()
    
    # Initialize tray icon
    result = True
    if not get_arg('no_tray'):
        log.info("Initializing tray icon")
        result = initialize_tray_icon()
    
    # Run without tray icon if it failed to initialize or if the user disabled it
    if not result or get_arg('no_tray'):
        log.info("Running without tray icon")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            log.info("Exiting WebDeck... (Ctrl+C)")
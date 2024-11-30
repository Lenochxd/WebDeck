import json
import os
import sys
import threading
import argparse
from .show_error import show_error
from .logger import log
from .exit import exit_program

temp_file = os.path.join("temp", "webdeck_args.json")
args = {}
raw_args = [arg for arg in sorted(sys.argv[1:]) if not (arg.endswith('.pyc') or arg.endswith('library.zip'))]
# log.debug(f"{raw_args=}")

available_args = {
    "-v": {
        "aliases": ["--version"],
        "help": "Display the application version and exit",
        "action": "store_true"
    },
    "-p": {
        "aliases": ["--port"],
        "help": "Specify a custom port for the Flask server",
        "type": int,
        "action": "store"
    },
    "-H": {
        "aliases": ["--host"],
        "help": "Specify the host for the Flask server",
        "type": str,
        "action": "store"
    },
    "-t": {
        "aliases": ["--timeout"],
        "help": "Specify the timeout in seconds to close the app after",
        "type": int,
        "action": "store"
    },
    "--no-admin": {
        "aliases": ["--no-sudo"],
        "help": "Run the application without requesting sudo/admin permissions",
        "action": "store_true"
    },
    "--no-tray": {
        "help": "Run the application without the system tray icon",
        "action": "store_true"
    },
    "--no-debug": {
        "help": "Disable the printing of debug messages (does not affect Flask debug mode)",
        "action": "store_true"
    },
    "--force-start": {
        "help": "Authorize the start of the app even if it is already running",
        "action": "store_true"
    },
    "--log-file": {
        "help": "Specify a custom log file path",
        "type": str,
        "action": "store"
    },
    "--force-update": {
        "aliases": ["--update"],
        "help": "Force update the application to the latest version",
        "action": "store_true"
    },
    "--no-auto-update": {
        "aliases": ["--no-update"],
        "help": "Disable the auto-update feature",
        "action": "store_true"
    },
    "--fake-error": {
        "help": "Simulate an error to test the error handling",
        "action": "store_true",
        "condition": not getattr(sys, 'frozen', False),
    },
}

positionals = {
    "exit": {
        "help": "Exit all instances of WebDeck running on the device",
        "choices": ["exit", "stop", "close", "quit", "kill", "terminate", "shutdown"],
        "nargs": "?",
        "default": None
    },
}


def parse_args():
    # Clear any previously saved arguments
    clear_args()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="WebDeck")
    
    # Add arguments to the parser
    for arg, arg_params in available_args.items():
        if not arg_params.get("condition", True):
            continue
        
        if "type" in arg_params:
            parser.add_argument(
                arg,
                *arg_params.get("aliases", []),
                help=arg_params.get("help"),
                type=arg_params["type"],
                action=arg_params.get("action", None),
            )
        else:
            parser.add_argument(
                arg,
                *arg_params.get("aliases", []),
                help=arg_params.get("help"),
                action=arg_params.get("action", None),
            )
    
    for arg, arg_params in positionals.items():
        parser.add_argument(
            arg,
            *arg_params.get("aliases", []),
            help=arg_params.get("help"),
            default=arg_params.get("default", None),
            nargs=arg_params.get("nargs", None),
            const=arg_params.get("const", None),
            action=arg_params.get("action", None),
        )
    
    try:
        # Parse the arguments
        parsed_args = parser.parse_args(raw_args)
        save_args(parsed_args)
        if not get_arg('no_debug') and not get_arg('version'):
            log.debug(f'All args: {parsed_args}')
    except Exception as e:
        log.error(f"Error parsing arguments: {e}")
        save_args(parser.parse_args([]))  # Save default arguments
    
    handle_startup_arguments()


def clear_args():
    # Remove the temporary arguments file if it exists
    if os.path.exists(temp_file):
        os.remove(temp_file)

def save_args(args):
    # Ensure the temp directory exists
    os.makedirs(os.path.dirname(temp_file), exist_ok=True)
    
    # Save arguments to a temporary file
    with open(temp_file, "w") as f:
        json.dump(vars(args), f)

def load_args():
    """
    Load arguments from the temporary file if available, otherwise return an empty dictionary.
    
    Returns:
        dict: A dictionary containing the loaded arguments.
    """
    global args
    
    if args:
        return args
    
    # Load arguments from the temporary file
    if os.path.exists(temp_file):
        with open(temp_file, "r") as f:
            args = json.load(f)
        os.remove(temp_file)  # Clean up after loading
        return args
    return {}

def get_arg(arg):
    """
    Retrieve the value of a specified argument from the loaded arguments.
    Args:
        arg (str): The name of the argument to retrieve.
    Returns:
        Union[str, bool, None]: The value of the specified argument if it exists, otherwise None.
    """
    
    return load_args().get(arg, None)


def handle_startup_arguments():
    # --no-debug
    if get_arg('no_debug'):
        log.disable_debug()
    
    # -V, --version
    if get_arg('version'):
        import json
        with open("webdeck/version.json", encoding="utf-8") as f:
            version = json.load(f)["versions"][0]["version"]
        
        last_commit = ""
        if not getattr(sys, 'frozen', False) and os.path.isdir(".git"):
            import subprocess
            try:
                last_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode('utf-8')
                last_commit = f"({last_commit[:7]})"
            except subprocess.CalledProcessError:
                pass
                # print("Could not retrieve the last commit.")
                
        print(f"WebDeck v{version} {last_commit}")
        sys.exit()
        

    # -T TIMEOUT, --timeout TIMEOUT
    timeout = get_arg('timeout')
    if timeout:
        try:
            timeout = int(timeout)
            log.info(f"Setting timeout to {timeout} seconds")
            threading.Timer(timeout, exit_program, kwargs={'force': True, 'from_timeout': True}).start()
        except ValueError:
            log.error("Invalid timeout value provided. It should be an integer.")
            exit_program(force=True, from_timeout=True)
    
    # --log-file
    log_file = get_arg('log_file')
    if log_file:
        log.set_log_file(log_file)
        log.info(f"Logging to file: {log_file}")
    
    # --fake-error
    if get_arg('fake_error'):
        try:
            1 / 0
        except Exception as e:
            import app.utils.languages as languages
            languages.init(
                lang_files_directory="webdeck/translations",
                misc_lang_files_directory="webdeck/translations/misc",
                default_language="en_US"
            )
            
            if os.name == 'nt':
                show_error(exception=e)
            else:
                log.exception(e, "Failed to initialize tray icon", expected=False)

    # exit
    if get_arg('exit'):
        if get_arg('exit') in positionals['exit']['choices']:
            exit_program(force=True)
        else:
            log.error("Invalid command provided.")
            exit_program(force=True)

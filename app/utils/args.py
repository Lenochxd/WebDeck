import json
import os
import argparse
from .logger import log

temp_file = os.path.join("temp", "webdeck_args.json")
args = {}

available_args = {
    "-V": {
        "aliases": ["--version"],
        "help": "Display the application version and exit",
        "action": "store_true"
    },
    "-P": {
        "aliases": ["--port"],
        "help": "Specify a custom port for the Flask server",
        "action": "store"
    },
    "-T": {
        "aliases": ["--timeout"],
        "help": "Specify the timeout in seconds to close the app after",
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
}

def parse_args():
    # Clear any previously saved arguments
    clear_args()
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="WebDeck")
    
    # Add arguments to the parser
    for arg, arg_params in available_args.items():
        parser.add_argument(
            arg,
            *arg_params.get("aliases", []),
            help=arg_params.get("help"),
            action=arg_params.get("action", None),
        )
    
    try:
        # Parse the arguments
        parsed_args = parser.parse_args()
        save_args(parsed_args)
        log.debug(f'All args: {parsed_args}')
    except Exception as e:
        log.error(f"Error parsing arguments: {e}")
        save_args(parser.parse_args([]))  # Save default arguments


def clear_args():
    # Remove the temporary arguments file if it exists
    if os.path.exists(temp_file):
        os.remove(temp_file)

def save_args(args):
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

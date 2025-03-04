import os
import sys
import json
from .exit import exit_program
from .logger import log
from .paths import TEMP_FILE


def restart_program():
    """Restarts the program, ensuring compatibility with frozen environments."""
    try:
        if getattr(sys, 'frozen', False):  # Check if the script is frozen
            # If frozen, restart using the bundled executable
            with open(TEMP_FILE, 'r') as f:
                temp_data = json.load(f)
            temp_data["allow_multiple_instances"] = True
            with open(TEMP_FILE, 'w') as f:
                json.dump(temp_data, f, indent=4)
                
            os.startfile(sys.executable)
        else:
            # If not frozen, restart the Python interpreter
            python = sys.executable
            os.execl(python, f'"{python}"', *sys.argv)
        exit_program()
    except Exception as e:
        log.exception(e, "Error while restarting the program")
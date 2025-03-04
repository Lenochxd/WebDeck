import psutil
import sys
import json
from .logger import log
from .platform import is_windows
from .paths import TEMP_FILE


def is_opened():
    # Check if the script is frozen
    if not getattr(sys, 'frozen', False):
        return False

    # Check and modify temp.json
    try:
        with open(TEMP_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
        log.info(f"{TEMP_FILE} file not found or invalid, creating a new one")

    if data.get('allow_multiple_instances', False):
        data['allow_multiple_instances'] = False
        try:
            with open(TEMP_FILE, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            log.exception(e, f"Error writing to {TEMP_FILE}")
        return False

    # Check running processes
    processes = [p.name().lower() for p in psutil.process_iter(["name"])]
    # log.debug(f"Running processes: {processes}")
    
    if is_windows:
        if "webdeck.exe" in processes:
            # Remove the current instance of webdeck.exe from the list of processes
            processes.remove("webdeck.exe")
    else:
        if "webdeck" in processes:
            # Remove the current instance of webdeck from the list of processes
            processes.remove("webdeck")
    
    return any("webdeck" in p for p in processes)

# tests
if __name__ == '__main__':
    print(is_opened())
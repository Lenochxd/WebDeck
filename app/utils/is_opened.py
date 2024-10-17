import psutil
import sys
import json


def is_opened():
    # Check if the script is frozen
    if not getattr(sys, 'frozen', False):
        return False

    # Check and modify temp.json
    try:
        with open('temp.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if data.get('allow_multiple_instances', False):
        data['allow_multiple_instances'] = False
        try:
            with open('temp.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error writing to temp.json: {e}")
        return False

    # Check running processes
    processes = [p.name().lower() for p in psutil.process_iter(["name"])]
    
    if "webdeck.exe" in processes:
        # Remove the current instance of webdeck.exe from the list of processes
        processes.remove("webdeck.exe")
    return any("webdeck" in p for p in processes)

# tests
if __name__ == '__main__':
    print(is_opened())
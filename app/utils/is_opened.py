import psutil
import sys


def is_opened():
    if not getattr(sys, 'frozen', False):
        return False
    
    processes = [p.name().lower() for p in psutil.process_iter(["name"])]

    if "webdeck.exe" in processes:
        processes.remove("webdeck.exe")
    return any("wd_" in p for p in processes) or any("webdeck" in p for p in processes)

# tests
if __name__ == '__main__':
    print(is_opened())
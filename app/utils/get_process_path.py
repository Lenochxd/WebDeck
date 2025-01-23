import os
import subprocess
from .platform import is_linux


def get_process_path(process_name):
    if not is_linux:
        return
    
    result = subprocess.run(["which", process_name], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    
    if os.path.exists(f"/lib/{process_name}"):
        return f"/lib/{process_name}"
    else:
        raise NotImplementedError("This function is not implemented for this platform")


xdotool = get_process_path("xdotool")
copyq = get_process_path("copyq")
xclip = get_process_path("xclip")

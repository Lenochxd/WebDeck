import os
import subprocess
from .platform import is_linux, is_wayland
from .working_dir import get_base_dir
from .logger import log


def get_process_path(process_name):
    if not is_linux:
        return None
    
    result = subprocess.run(["which", process_name], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    
    lib_path = os.path.join(get_base_dir(), "lib", process_name)
    if os.path.exists(lib_path):
        return os.path.abspath(lib_path)
    return None


def require_process_path(process_name):
    process_path = get_process_path(process_name)
    if process_path is None:
        raise RuntimeError(f"Required process not found: {process_name}")
    return process_path


if not is_wayland:
    xdotool = get_process_path("xdotool")
    copyq = get_process_path("copyq")
xclip = get_process_path("xclip")

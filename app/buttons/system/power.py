from app.utils.platform import is_windows, is_linux, is_mac
import subprocess


def shutdown():
    if is_windows:
        subprocess.Popen("shutdown /s /f /t 0", shell=True)
    elif is_linux:
        subprocess.Popen("poweroff", shell=True)

def restart():
    if is_windows:
        subprocess.Popen("shutdown /r /f /t 0", shell=True)
    elif is_linux:
        subprocess.Popen("reboot", shell=True)

def sleep():
    if is_windows:
        subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
    elif is_linux:
        subprocess.Popen("systemctl suspend", shell=True)

def hibernate():
    if is_windows:
        subprocess.Popen("shutdown /h /t 0", shell=True)
    elif is_linux:
        subprocess.Popen("systemctl hibernate", shell=True)

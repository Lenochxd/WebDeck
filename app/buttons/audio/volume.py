import time
import math
import ctypes
import win32api
import win32con
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume



def get_current_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    return volume.GetMasterVolumeLevelScalar()


def set_volume(target_volume):
    current_volume = get_current_volume()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    while math.isclose(current_volume, target_volume, rel_tol=0.01) == False:
        if current_volume > target_volume:
            current_volume -= 0.01
        else:
            current_volume += 0.01
        volume.SetMasterVolumeLevelScalar(current_volume, None)
        time.sleep(0.01)

    return current_volume


def increase_volume(delta):
    win32api.keybd_event(win32con.VK_VOLUME_UP, 0)
    win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP)
    if delta == "":
        return get_current_volume()
    target_volume = get_current_volume() + (int(delta) / 100.0)
    return set_volume(target_volume)


def decrease_volume(delta):
    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0)
    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP)
    if delta == "":
        return get_current_volume()
    target_volume = get_current_volume() - (int(delta) / 100.0)
    return set_volume(target_volume)


def handle_command(message):
    if message.startswith("/volume +"):
        delta = message.replace("/volume +", "")
        if delta.replace(" ","") == "":
            increase_volume("1")
        else:
            increase_volume(delta)
            
    elif message.startswith("/volume -"):
        delta = message.replace("/volume -", "")
        if delta.replace(" ","") == "":
            decrease_volume("1")
        else:
            decrease_volume(delta)
            
    elif message.startswith("/volume set"):
        target_volume = int(message.replace("/volume set ", "")) / 100.0
        set_volume(target_volume)
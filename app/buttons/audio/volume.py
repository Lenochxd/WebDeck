from app.utils.platform import is_windows, is_linux

import time
import math
import ctypes
import keyboard
import os
if not is_linux or os.environ.get("DISPLAY"):
    import pyautogui
if is_windows:
    import win32api
    import win32con
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
else:
    from pulsectl import Pulse

from app.utils.logger import log



def get_current_volume():
    if is_windows:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
        return volume.GetMasterVolumeLevelScalar()
    
    elif is_linux:
        with Pulse('volume') as pulse:
            sink = pulse.sink_list()[0]
            return round(sink.volume.value_flat, 2)
    
    else:
        raise NotImplementedError("This command is not implemented for this platform")


def set_volume(target_volume):
    if is_windows:
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
    
    elif is_linux:
        with Pulse('volume') as pulse:
            sink = pulse.sink_list()[0]
            volume = sink.volume
            volume.value_flat = target_volume
            pulse.volume_set(sink, volume)
            return target_volume
    
    else:
        raise NotImplementedError("This command is not implemented for this platform.")


def increase_volume(delta=1):
    if is_windows:
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0)
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP)
        if delta == "":
            return get_current_volume()
        target_volume = get_current_volume() + (int(delta) / 100.0)
        return set_volume(target_volume)
    
    elif is_linux:
        with Pulse('volume') as pulse:
            sink = pulse.sink_list()[0]
            target_volume = min(sink.volume.value_flat + (int(delta) / 100.0), 1.0)
            volume = sink.volume
            volume.value_flat = target_volume
            pulse.volume_set(sink, volume)
            return target_volume
    
    else:
        raise NotImplementedError("This command is not implemented for this platform.")


def decrease_volume(delta=1):
    if is_windows:
        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0)
        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP)
        if delta == "":
            return get_current_volume()
        target_volume = get_current_volume() - (int(delta) / 100.0)
        return set_volume(target_volume)
    
    elif is_linux:
        with Pulse('volume') as pulse:
            sink = pulse.sink_list()[0]
            target_volume = max(sink.volume.value_flat - (int(delta) / 100.0), 0.0)
            volume = sink.volume
            volume.value_flat = target_volume
            pulse.volume_set(sink, volume)
            return target_volume
    
    else:
        raise NotImplementedError("This command is not implemented for this platform.")


def mute_volume():
    if is_windows:
        try:
            keyboard.send("volume mute")
        except Exception:
            try:
                keyboard.send(-173)
            except Exception:
                pyautogui.press("volumemute")
    
    elif is_linux:
        try:
            keyboard.send("volume mute")
        except Exception:
            keyboard.send(113)
    
    else:
        raise NotImplementedError("This command is not implemented for this platform.")


def handle_command(message):
    if message.startswith("/volume +"):
        delta = message.replace("/volume +", "").strip()
        delta = int(delta) if delta else 1
        increase_volume(delta)
            
    elif message.startswith("/volume -"):
        delta = message.replace("/volume -", "").strip()
        delta = int(delta) if delta else 1
        decrease_volume(delta)
            
    elif message.startswith("/volume set"):
        target_volume = int(message.replace("/volume set ", "")) / 100.0
        set_volume(target_volume)
        
    elif message.startswith("/volume mute"):
        mute_volume()

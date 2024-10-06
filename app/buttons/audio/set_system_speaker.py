import pyaudio
import win32api
import win32con


p = pyaudio.PyAudio()
def set_speakers_by_name(speakers_name):
    # TODO: (not working rn)
    device_count = p.get_device_count()

    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        if device_info["name"].lower().find(speakers_name.lower()) != -1:
            # Select the found audio device
            win32api.SendMessage(
                win32con.HWND_BROADCAST,
                win32con.WM_APPCOMMAND,
                0,
                win32api.LPARAM(0x30292),
            )
            win32api.SendMessage(
                win32con.HWND_BROADCAST,
                win32con.WM_APPCOMMAND,
                0,
                win32api.LPARAM(0x30290 + i),
            )
            break
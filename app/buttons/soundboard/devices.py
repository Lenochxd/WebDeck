try: import vlc
except: pass

def get_device(device):
    # https://stackoverflow.com/questions/73884593/how-to-change-vlc-python-output-device
    try:
        player = vlc.MediaPlayer()
        mods = player.audio_output_device_enum()
        if mods:
            mod = mods
            while mod:
                mod = mod.contents
                # If device (VB-Cable) is found, return it's module and device id
                if device.lower() in str(mod.description).lower():
                    device = mod.device
                    return device
                mod = mod.next
    except Exception as e:
        print(e)
        return "ERROR_NO_VLC"
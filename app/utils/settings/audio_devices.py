import pyaudio
from ..logger import log

def get_audio_devices(channels_type="input"):
    p = pyaudio.PyAudio()
    all_devices = []

    try:
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)

            if channels_type == "input":
                channels = device_info["maxInputChannels"]
            else:
                channels = device_info["maxOutputChannels"]
            # Vérifier si le périphérique est un périphérique d'entrée actif
            if channels > 0 and device_info["hostApi"] == 0:
                ok = True
                for device in all_devices:
                    if (
                        device[device.find("(") + 1 :]
                        in device_info["name"][device_info["name"].find("(") + 1 :]
                    ):
                        ok = False
                if ok and not "microsoft - input" in device_info["name"].lower():
                    # log.debug(f"Device {i}: {device_info['name']}")
                    all_devices.append(device_info["name"])
        del ok
        # log.debug(f"Total number of audio devices found: {len(all_devices)}")
        # log.debug(f"Default output device info: {p.get_default_output_device_info()}")
    except Exception as e:
        log.exception(e, "An error has occurred while retrieving audio devices")
    finally:
        p.terminate()
    return all_devices
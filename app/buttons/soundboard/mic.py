import pyaudio
import time
import threading

from .devices import get_device
from app.utils.load_config import load_config


sb_on = True
def soundboard():
    global sb_on
    sb_on = True
    config = load_config()

    audio = pyaudio.PyAudio()
    num_devices = audio.get_device_count()

    mic_input_device = config["settings"]["soundboard"]["mic_input_device"]
    microphone_name = mic_input_device[mic_input_device.find("(") + 1 :]
    mic_output_device = config["settings"]["soundboard"]["vbcable"]
    output_name = mic_output_device[mic_output_device.find("(") + 1 :]
    mic_index = None
    output_device = None

    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if (
            device_info["maxInputChannels"] > 0
            and microphone_name.lower() in device_info["name"].lower()
        ):
            mic_index = i
            break

    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if (
            device_info["maxOutputChannels"] > 0
            and output_name.lower() in device_info["name"].lower()
        ):
            output_device = i
            break

    if mic_index is None:
        print("Cannot find microphone.")
    else:
        print(f"Microphone '{microphone_name}' found at index {mic_index}")

    if output_device is None:
        print("Cannot find speakers.")
    else:
        print(f"Speaker '{output_name}' found at index {output_device}")

    stream_in = None
    stream_out = None

    input_device_info = audio.get_device_info_by_index(mic_index)
    input_channels = input_device_info["maxInputChannels"]

    output_device_info = audio.get_device_info_by_index(output_device)
    output_channels = input_device_info["maxInputChannels"]

    print(f"i: {input_device_info}")
    print(f"o: {output_device_info}")

    stream_in = audio.open(
        format=pyaudio.paInt16,
        channels=input_channels,
        rate=44100,
        input=True,
        input_device_index=mic_index,
    )

    stream_out = audio.open(
        format=pyaudio.paInt16,
        channels=input_channels,
        rate=44100,
        output=True,
        output_device_index=output_device,
    )

    print("soundboard: ON")

    try:
        while sb_on:
            data = stream_in.read(1024)
            stream_out.write(data)
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping soundboard ...")

        try:
            if stream_in is not None:
                stream_in.stop_stream()
                stream_in.close()

            if stream_out is not None:
                stream_out.stop_stream()
                stream_out.close()
        except OSError:
            restart()

        audio.terminate()


def stop():
    global sb_on
    sb_on = False

def restart():
    global soundboard_thread,cable_input_device, sb_on
    config = load_config()
    cable_input_device = get_device(config["settings"]["soundboard"]["vbcable"])
    
    sb_on = False
    time.sleep(0.2)
    soundboard_thread = threading.Thread(target=soundboard, daemon=True)
    soundboard_thread.start()
    print("Soundboard thread revived")


# mic thread
config = load_config()
if config["settings"]["soundboard"]["enabled"] == "true":
    soundboard_thread = threading.Thread(target=soundboard, daemon=True)
    soundboard_thread.start()
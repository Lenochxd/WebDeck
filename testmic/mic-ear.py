import pyaudio

def main():
    mic_index = None
    speaker_index = None

    audio = pyaudio.PyAudio()
    num_devices = audio.get_device_count()

    mic_index = 2
    
    speaker_index = 5

    if mic_index is None:
        print("Impossible de trouver le microphone.")
        return

    if speaker_index is None:
        print("Impossible de trouver les haut-parleurs.")
        return

    stream_in = None
    stream_out = None

    try:
        stream_in = audio.open(format=pyaudio.paInt16,
                               channels=1,
                               rate=44100,
                               input=True,
                               input_device_index=mic_index)
    except Exception:
        stream_in = audio.open(format=pyaudio.paInt16,
                               channels=2,
                               rate=44100,
                               input=True,
                               input_device_index=mic_index)

    try:
        stream_out = audio.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=44100,
                                output=True,
                                output_device_index=speaker_index)
    except Exception:
        stream_out = audio.open(format=pyaudio.paInt16,
                                channels=2,
                                rate=44100,
                                output=True,
                                output_device_index=speaker_index)

    print("En cours d'enregistrement... (Appuyez sur Ctrl+C pour arrêter)")

    try:
        while True:
            data = stream_in.read(1024)
            stream_out.write(data)
    except KeyboardInterrupt:
        pass
    finally:
        print("Arrêt de l'enregistrement.")

        if stream_in is not None:
            stream_in.stop_stream()
            stream_in.close()

        if stream_out is not None:
            stream_out.stop_stream()
            stream_out.close()

        audio.terminate()


if __name__ == '__main__':
    main()

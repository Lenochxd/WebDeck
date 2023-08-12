import pyaudio
import struct

# Paramètres de l'enregistrement audio
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

# Paramètres d'amplification du microphone
AMPLITUDE_FACTOR = 1.0

# Trouver l'index du microphone et du nouvel appareil microphone virtuel
MIC_NAME = 'Razer Barracuda X Microphone'
NEW_MIC_NAME = 'Razer Barracuda X Microphone'
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    if MIC_NAME.lower() in dev_info['name'].lower():
        mic_idx = dev_info['index']
        print(f"Microphone trouvé: {dev_info['name']}")
    elif NEW_MIC_NAME.lower() in dev_info['name'].lower():
        new_mic_idx = dev_info['index']
        print(f"Microphone trouvé: {dev_info['name']}")

# Ouvrir le stream d'entrée du microphone
stream_in = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK,
                   input_device_index=mic_idx)

# Ouvrir le stream de sortie du nouvel appareil microphone virtuel
stream_out = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK,
                    output_device_index=new_mic_idx)

# Boucle principale d'enregistrement audio
while True:
    # Lire les données du microphone
    data = stream_in.read(CHUNK)

    # Amplifier les données si nécessaire
    if AMPLITUDE_FACTOR != 1:
        data_bytes = struct.unpack(f"{CHUNK * CHANNELS}h", data)
        amplified_data_bytes = [max(min(int(sample * AMPLITUDE_FACTOR), 32767), -32768) for sample in data_bytes]
        data = struct.pack(f"{CHUNK * CHANNELS}h", *amplified_data_bytes)

    # Écrire les données sur le nouvel appareil microphone virtuel
    stream_out.write(data)

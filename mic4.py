import pyaudio
import struct

MIC_NAME = "Razer Barracuda X Mic"
SPK_NAME = "CABLE In"
AMPLITUDE_FACTOR = 100

p = pyaudio.PyAudio()

mic_idx = None
spk_idx = None

# Trouver les index du microphone et du casque
for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    if MIC_NAME in dev_info['name']:
        mic_idx = dev_info['index']
        print(f"Microphone trouvé: {dev_info['name']}")
        break
for i in range(p.get_device_count()):
    dev_info = p.get_device_info_by_index(i)
    if SPK_NAME in dev_info['name'] and not "microphone" in dev_info['name'].lower():
        spk_idx = dev_info['index']
        print(f"Casque trouvé: {dev_info['name']}")
        break

# Configurer les paramètres audio
format = pyaudio.paInt16
channels = p.get_device_info_by_index(mic_idx)['maxInputChannels']
sample_rate = int(p.get_device_info_by_index(mic_idx)['defaultSampleRate'])
frames_per_buffer = 1024

# Ouvrir les flux audio pour le microphone et le casque
mic_stream = p.open(format=format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=frames_per_buffer,
                    input_device_index=mic_idx)

spk_stream = p.open(format=format,
                    channels=channels,
                    rate=sample_rate,
                    output=True,
                    frames_per_buffer=frames_per_buffer,
                    output_device_index=spk_idx)

# Boucle de transfert audio du microphone au casque
while True:
    data = mic_stream.read(frames_per_buffer)
    # Convertir les données audio en bytes
    data_bytes = struct.unpack(f"{frames_per_buffer * channels}h", data)
    # Multiplier chaque échantillon par le facteur d'amplitude en limitant les valeurs à la plage valide
    amplified_data_bytes = [max(min(int(sample * AMPLITUDE_FACTOR), 32767), -32768) for sample in data_bytes]

    # Convertir les bytes amplifiés en données audio
    amplified_data = struct.pack(f"{frames_per_buffer * channels}h", *amplified_data_bytes)
    # Écrire les données audio amplifiées dans le flux de sortie du casque
    spk_stream.write(amplified_data)

# Fermer les flux audio et PyAudio
mic_stream.stop_stream()
mic_stream.close()
spk_stream.stop_stream()
spk_stream.close()
p.terminate()
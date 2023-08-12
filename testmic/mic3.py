import sounddevice as sd
import numpy as np

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

# Récupérer l'indice du périphérique de microphone
mic_list = sd.query_devices()
mic_index = None
for i, mic in enumerate(mic_list):
    if 'Razer' in mic['name']:
        mic_index = i
        break

# Récupérer l'indice du périphérique de sortie (VBCABLE)
vb_list = sd.query_devices()
vb_index = None
for i, vb in enumerate(vb_list):
    if 'CABLE Input' in vb['name']:
        vb_index = i
        break

if mic_index is None:
    raise ValueError("Le microphone n'a pas été trouvé")

if vb_index is None:
    raise ValueError("Le périphérique de sortie n'a pas été trouvé")

# Nombre de canaux du micro et du VBCABLE
mic_channels = mic_list[mic_index]['max_input_channels']
vb_channels = vb_list[vb_index]['max_output_channels']

if mic_channels == 1 and vb_channels == 1:
    channels = 1
else:
    channels = 2
    print(mic_channels, vb_channels)

# Ouvrir le stream audio avec les paramètres choisis
with sd.Stream(device=mic_index, blocksize=1024, callback=callback, dtype='int16', channels=channels):
    sd.default.channels = channels
    print("Le stream audio a été ouvert avec succès")
    input()

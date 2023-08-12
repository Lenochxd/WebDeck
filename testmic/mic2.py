
import os
from pathlib import Path
if not Path('temp/mic-temp').is_file():
    with open('temp/mic-temp', 'w') as f:
        f.write('')
        
        
    import pyaudio
    import time
    
    time.sleep(1)
    try: os.remove('temp/mic-temp')
    except: pass

    # Initialise PyAudio
    p = pyaudio.PyAudio()
    
    num_output_devices = p.get_device_count()

    # Parcourez chaque périphérique d'entrée et imprimez ses informations
    for i in range(num_output_devices):
        device_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']}")
        if "Razer Barracuda X Microphone" in device_info['name']:
            # Sélectionnez le microphone de votre choix en utilisant l'index du périphérique
            mic_index = int(i)
            break
    print("in: ", mic_index)
    
    # Obtenir les informations par défaut du microphone sélectionné
    def_mic_info = p.get_device_info_by_index(mic_index)
    
    def_mic_info['defaultSampleRate'] = 44100
    
    # Ouvrir le microphone sélectionné en utilisant PyAudio
    try:
        mic = p.open(format=pyaudio.paInt24,
                    channels=2,
                    rate=44100,
                    input_device_index=mic_index,
                    input=True)
    except Exception as e:
        if "Invalid number of channels" in str(e):
            mic = p.open(format=pyaudio.paInt24,
                    channels=1,
                    rate=44100,
                    input_device_index=mic_index,
                    input=True)
        else: print(e)
    
    # Obtenir les informations par défaut du VBCABLE
    def_vb_info = p.get_default_output_device_info()
    print(def_vb_info)
    
    # Obtenir l'index du VBCABLE
    for i in range(num_output_devices):
        device_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']}")
        if "CABLE In" in device_info['name']:
            # Sélectionnez l'haut parleur VBCABLE en utilisant l'index du périphérique
            vb_index = int(i)
            break
    print("out: ", vb_index)
    def_mic_info['defaultSampleRate'] = 48000
    
    # Ouvrir le VBCABLE en utilisant PyAudio
    try:
        vb = p.open(format=pyaudio.paInt24,
                    channels=2,
                    rate=int(def_vb_info['defaultSampleRate']),
                    output_device_index=vb_index,
                    output=True)
    except Exception as e:
        if "Invalid number of channels" in str(e):
            vb = p.open(format=pyaudio.paInt24,
                    channels=1,
                    rate=int(def_vb_info['defaultSampleRate']),
                    output_device_index=vb_index,
                    output=True)
        else: print(e)
    
    # Boucle pour lire les données du flux audio du microphone et les écrire dans le flux audio du VBCABLE
    while True:
        try:
            # Lisez le son du microphone
            data = mic.read(4096)
            # Envoyez le son vers l'haut parleur VBCABLE
            vb.write(data)
        except KeyboardInterrupt:
            # Quittez la boucle lorsque l'utilisateur appuie sur Ctrl+C
            break

    # Fermez les périphériques audio
    mic.stop_stream()
    mic.close()
    vb.stop_stream()
    vb.close()

    # Terminez PyAudio
    p.terminate()

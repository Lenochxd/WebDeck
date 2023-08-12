
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
        if "Microphone (Razer Barracuda X)" in device_info['name']:
            # Sélectionnez le microphone de votre choix en utilisant l'index du périphérique
            mic_index = int(i)
            break
    print("in: ", mic_index)

    # Ouvrez le microphone sélectionné en utilisant PyAudio
    device_info = p.get_device_info_by_index(mic_index)
    print("1: ",device_info)
    sample_rate = device_info['defaultSampleRate']
    if sample_rate <= 16000:
        format_1 = pyaudio.paInt16
    elif sample_rate <= 32000:
        format_1 = pyaudio.paInt16
    else:
        format_1 = pyaudio.paInt16
    print("format_1: ", format_1)
    format_1 = pyaudio.paInt16
    print("format_1: ", format_1)
    sample_rate = int(sample_rate)
    try:
        mic = p.open(format=format_1,
                     channels=2,
                     rate=sample_rate,
                     input_device_index=mic_index,
                     input=True)
    except Exception as e:
        if "Invalid number of channels" in str(e):
            mic = p.open(format=format_1,
                     channels=1,
                     rate=sample_rate,
                     input_device_index=mic_index,
                     input=True)
        


    # Parcourez chaque périphérique de sortie et imprimez ses informations
    for i in range(num_output_devices):
        device_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']}")
        if "CABLE In" in device_info['name']:
            # Sélectionnez l'haut parleur VBCABLE en utilisant l'index du périphérique
            vb_index = int(i)
            break
    print("out: ", vb_index)

    # Ouvrez l'haut parleur VBCABLE en utilisant PyAudio
    
    # Récupère les informations du périphérique de sortie VBCABLE
    device_info = p.get_device_info_by_index(vb_index)
    print("2: ", device_info)
    
    sample_rate2 = device_info['defaultSampleRate']
    if sample_rate2 <= 16000:
        format_ = pyaudio.paInt16
    elif sample_rate2 <= 32000:
        format_ = pyaudio.paInt16
    else:
        format_ = pyaudio.paInt16
    print("format_: ", format_)
    format_ = pyaudio.paInt16
    print("format_: ", format_)
    sample_rate2 = int(sample_rate2)
    try:
        vb = p.open(format=format_,
                     channels=2,
                     rate=sample_rate2,
                     output_device_index=vb_index,
                     output=True)
    except Exception as e:
        if "Invalid number of channels" in str(e):
            vb = p.open(format=format_,
                     channels=1,
                     rate=sample_rate2,
                     output_device_index=vb_index,
                     output=True)
        else: print(e)

    mic.start_stream()
    vb.start_stream()
    # Boucle infinie pour lire et envoyer le son du microphone vers l'haut parleur VBCABLE
    while True:
        try:
            # Lisez le son du microphone
            data = mic.read(1024)
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

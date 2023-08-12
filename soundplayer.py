from time import sleep
import pygame
import pygame._sdl2.audio as sdl2_audio

def get_devices(capture_devices: bool = False) -> tuple[str, ...]:
    init_by_me = not pygame.mixer.get_init()
    if init_by_me:
        pygame.mixer.init()
    devices = tuple(sdl2_audio.get_audio_device_names(capture_devices))
    if init_by_me:
        pygame.mixer.quit()
    for d in devices:
        if "virtual cable" in d.lower():
            device = d
    return device

def play(file_path: str, device = None):
    if device is None:
        device = get_devices()
    print("Play: {}\r\nDevice: {}".format(file_path, device))
    pygame.mixer.init(devicename=device)
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    pygame.mixer.quit()
play("static/files/sounds/Cypis - Gdzie jest biały węgorz  (Zejście).mp3")
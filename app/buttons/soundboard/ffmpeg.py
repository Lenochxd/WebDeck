import os
from pathlib import Path
from pydub import AudioSegment
import urllib.request
import zipfile
import subprocess
import shutil
from app.utils.logger import log


is_downloading = False
ffmpeg_path = ""

def install_ffmpeg():
    global is_downloading, ffmpeg_path
    
    # Check if ffmpeg is already installed in the system
    if ffmpeg_path and os.path.isfile(ffmpeg_path):
        return ffmpeg_path
    
    # Check if ffmpeg is already installed in the current directory
    if os.path.isfile("ffmpeg.exe"):
        return os.path.abspath("ffmpeg.exe")

    # Search for ffmpeg installation on winget
    try:
        base_path = Path("C:/Users")

        # Iterate through user directories
        for user_dir in base_path.iterdir():
            if user_dir.is_dir():
                # Iterate through subdirectories of the user directory
                for package_dir in user_dir.joinpath("AppData/Local/Microsoft/WinGet/Packages").iterdir():
                    if package_dir.name.startswith("Gyan.FFmpeg"):
                        # Iterate through subdirectories of the package
                        for sub_dir in package_dir.iterdir():
                            if sub_dir.is_dir() and sub_dir.name.startswith("ffmpeg-"):
                                # Find the ffmpeg.exe file
                                ffmpeg_path = sub_dir.joinpath("bin/ffmpeg.exe")
                                # Check if the file exists
                                if ffmpeg_path.exists():
                                    log.debug(f"ffmpeg path found: {ffmpeg_path}")
                                    return str(ffmpeg_path)
                        continue
                continue
    except Exception as e:
        log.exception(e, "FFMPEG: Error occurred during search for ffmpeg installation via WinGet")


    # Install ffmpeg via webdeck servers
    try:
        if not is_downloading:
            is_downloading = True
            
            log.info("FFMPEG: downloading ffmpeg using webdeck servers...")
            url = "https://bishokus.fr/dl_ffmpeg"
            zip_path = "ffmpeg-N-114554-g7bf85d2d3a-win64-gpl.zip"
            urllib.request.urlretrieve(url, zip_path)
            
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall("")
                
            os.remove(zip_path)
            is_downloading = False
            return os.path.abspath("ffmpeg.exe")
    except Exception as e:
        log.exception(e, "FFMPEG: Error occurred while downloading ffmpeg using webdeck servers")
    
    # Install ffmpeg via winget
    if not is_downloading:
        try:
            log.info("FFMPEG: downloading ffmpeg using winget...")
            subprocess.Popen("winget install ffmpeg", shell=True).wait()
            return install_ffmpeg()
        except Exception as e:
            log.exception(e, "FFMPEG: Error occurred while downloading ffmpeg using winget")
        finally:
            is_downloading = False
    
    log.error("FFMPEG: not found.")
    return None

def get_ffmpeg():
    ffmpeg_path = install_ffmpeg()
    
    if ffmpeg_path is not None:
        if os.path.abspath(ffmpeg_path) != os.path.abspath("ffmpeg.exe"):
            shutil.copyfile(ffmpeg_path, "ffmpeg.exe")
        if os.path.abspath(ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe')) != os.path.abspath("ffprobe.exe"):
            shutil.copyfile(ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe'), "ffprobe.exe")
        
        ffmpeg_path = os.path.abspath("ffmpeg.exe")
        ffprobe_path = ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe')

        AudioSegment.converter = ffmpeg_path
        AudioSegment.ffmpeg = ffmpeg_path
        AudioSegment.ffprobe = ffprobe_path
    return ffmpeg_path


def replace_last_element(string, old_element, new_element):
    # Find the last occurrence of the old element
    last_index = string.rfind(old_element)

    if last_index != -1:  # If the old element is found
        return string[:last_index] + string[last_index:].replace(
            old_element, new_element, 1
        )
    else:
        # If the old element is not found, return the original string
        return string

def add_silence_to_end(input_file, output_file, silence_duration_ms=2000):
    global ffmpeg_path
    
    try:
        audio = AudioSegment.from_mp3(os.path.abspath(input_file))
    except FileNotFoundError as e:
        log.exception(e, "Error occurred while loading the audio file")
        ffmpeg_path = get_ffmpeg()
        
        if ffmpeg_path is None:
            return False

    silent_segment = AudioSegment.silent(duration=silence_duration_ms)
    audio_with_silence = audio + silent_segment
    audio_with_silence.export(output_file, format="mp3")

    return True

def silence_path(input_file, remove_previous=False):
    
    output_file = replace_last_element(input_file, ".mp3", "_.mp3")
    if os.path.exists(output_file):
        return input_file
    result = add_silence_to_end(input_file, output_file, 2)
    if result == False:
        return False
    
    if remove_previous:
        os.remove(input_file)

    return output_file


def to_wav(input_file: str, output_file: str=None, volume: float=0.5):
    global ffmpeg_path
    ffmpeg_path = get_ffmpeg()
    
    # Set default output file name if not provided
    if not output_file:
        output_file = replace_last_element(input_file, ".mp3", f"_vol{int(volume*100)}.wav")
    
    # Check if the output file already exists
    if os.path.exists(output_file):
        return output_file
    
    try:
        # Load the audio file
        audio = AudioSegment.from_file(os.path.abspath(input_file))
    except FileNotFoundError as e:
        log.exception(e, "Error occurred while loading the audio file")
        if ffmpeg_path is None:
            return False

    # Adjust volume
    audio = audio + (volume * 10)  # pydub uses dB for volume adjustment
    
    # Export as WAV
    audio.export(output_file, format="wav")
    return output_file
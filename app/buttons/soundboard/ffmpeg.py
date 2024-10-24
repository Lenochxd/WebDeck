import os
from pathlib import Path
from pydub import AudioSegment
import urllib.request
import zipfile
import subprocess
import shutil
from app.utils.logger import log


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


def get_ffmpeg():
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
    
    # Search for ffmpeg installation via webdeck servers
    if os.path.isfile("ffmpeg.exe"):
        return "ffmpeg.exe"

    try:
        log.info("FFMPEG: downloading ffmpeg using webdeck servers...")
        url = "https://bishokus.fr/dl_ffmpeg"
        urllib.request.urlretrieve(url, "ffmpeg-N-114554-g7bf85d2d3a-win64-gpl.zip")
        
        with zipfile.ZipFile("ffmpeg-N-114554-g7bf85d2d3a-win64-gpl.zip", "r") as zip_ref:
            zip_ref.extractall("")
            
        os.remove("ffmpeg-N-114554-g7bf85d2d3a-win64-gpl.zip")
        return "ffmpeg.exe"
    except Exception as e:
        log.exception(e, "FFMPEG: Error occurred while downloading ffmpeg using webdeck servers")
    
        log.info("FFMPEG: downloading ffmpeg using winget...")
        subprocess.Popen("winget install ffmpeg", shell=True)
    
    log.error("FFMPEG: not found.")
    return None
    

ffmpeg_path = ""
def add_silence_to_end(input_file, output_file, silence_duration_ms=2000):
    global ffmpeg_path
    
    try:
        audio = AudioSegment.from_mp3(os.path.abspath(input_file))
    except FileNotFoundError as e:
        log.exception(e, "Error occurred while loading the audio file")
        ffmpeg_path = get_ffmpeg()
        
        if ffmpeg_path is not None and ffmpeg_path != "ffmpeg.exe":
            shutil.copyfile(ffmpeg_path, "ffmpeg.exe")
            shutil.copyfile(ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe'), "ffprobe.exe")
            
            ffmpeg_path = os.path.abspath("ffmpeg.exe")
            ffprobe_path = ffmpeg_path.replace('ffmpeg.exe', 'ffprobe.exe')

            AudioSegment.converter = ffmpeg_path
            AudioSegment.ffmpeg = ffmpeg_path
            AudioSegment.ffprobe = ffprobe_path
        if AudioSegment.converter is None:
            return False
    else:
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
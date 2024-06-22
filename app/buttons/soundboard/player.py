try: import vlc
except: pass
from flask import jsonify

from app.utils.load_config import load_config
from app.utils.load_lang_file import load_lang_file

from .devices import get_device
from .ffmpeg import silence_path


config = load_config()
text = load_lang_file(config["settings"]["language"])
cable_input_device = get_device(config["settings"]["soundboard"]["vbcable"])
vlc_installed = cable_input_device != "ERROR_NO_VLC"

player_vbcable = {}
player_local = {}

def get_params(msg):
    message = msg.replace("C:\\fakepath\\", "").replace("/playsound ", "").replace("/playlocalsound ", "")
    percentage = message[message.rfind(" ") + 1 :].replace(" ", "")
    try:
        sound_volume = float(percentage) / 100
        sound_file = message.replace("/playsound ", "").replace("/playlocalsound ", "").replace(percentage, "")
    except:
        sound_volume = float(50) / 100  # mid volume (default)
        sound_file = message.replace("/playsound ", "").replace("/playlocalsound ", "")

    if all(
        substring not in sound_file
        for substring in [
            ":",
            ".config/user_uploads/",
            ".config\\user_uploads\\",
        ]
    ):
        # if it is stored directly in .config/user_uploads and not in C:\example
        sound_file = f".config/user_uploads/{sound_file}"

    if msg.startswith("/playlocalsound"):
        localonly = True
        ear_soundboard = True
    else:
        localonly = False
        ear_soundboard = config["settings"]["ear-soundboard"]
        
    
    return sound_file, sound_volume, ear_soundboard, localonly


def playsound(file_path: str, sound_volume=0.5, ear_soundboard=True, localonly=False):

    global cable_input_device, player_vbcable, player_local
    
    if not vlc_installed:
        print("VLC is not installed!")
        return jsonify({"success": False, "message": text["vlc_not_installed_error"]})
    else:
        if config["settings"]["fix-stop-soundboard"]:
            file_path = silence_path(file_path)
            if file_path == False:
                return jsonify({"success": False, "message": text["ffmpeg_not_installed_error"]})
            
        print(f"Play: {file_path}  -  volume:{sound_volume}\r\n")
        print(len(player_vbcable))
        print(player_vbcable)

        p_id = max(
            len(player_vbcable.keys()), len(player_local.keys())
        )
            
        if p_id <= 3:
            if not localonly:
                player_vbcable[p_id] = vlc.MediaPlayer(file_path)
                player_vbcable[p_id].audio_set_volume(int(sound_volume * 100))
                player_vbcable[p_id].audio_output_device_set(None, cable_input_device)
                player_vbcable[p_id].play()
                player_vbcable[p_id].event_manager().event_attach(
                    vlc.EventType.MediaPlayerEndReached, lambda x: remove_player(1, p_id)
                )

            if ear_soundboard or localonly == True:
                player_local[p_id] = vlc.MediaPlayer(file_path)
                player_local[p_id].audio_set_volume(int(sound_volume * 100))
                player_local[p_id].play()
                player_local[p_id].event_manager().event_attach(
                    vlc.EventType.MediaPlayerEndReached,
                    lambda x: remove_player(2, p_id),
                )

        else:
            if not localonly:
                player_vbcable[0].stop()
                player_vbcable[0].set_time(0)
                player_vbcable[0].play()
                player_vbcable[0].event_manager().event_attach(
                    vlc.EventType.MediaPlayerEndReached, lambda x: remove_player(1, p_id)
                )

            if ear_soundboard or localonly == True:
                player_local[0].stop()
                player_local[0].set_time(0)
                player_local[0].play()
                player_local[0].event_manager().event_attach(
                    vlc.EventType.MediaPlayerEndReached,
                    lambda x: remove_player(2, p_id),
                )
        
        print('local:', player_local)
        print('vbcab:', player_vbcable)
        
        return jsonify({"success": True})
    

def stopsound():
    if not vlc_installed:
        print("VLC is not installed!")
        return jsonify({"success": False, "message": text["vlc_not_installed_error"]})
    else:
        global player_vbcable, player_local
        
        try:
            if len(player_vbcable.keys()) > len(player_local.keys()):
                last_key = list(player_vbcable.keys())[-1]
                last_value = player_vbcable[last_key]
            else:
                last_key = list(player_local.keys())[-1]
                last_value = player_local[last_key]
        except IndexError:
            return jsonify({"success": True, "message": "There are no sounds actually playing"})
        
        while str(last_value.get_state()) == "State.Playing":
            print(player_vbcable)
            print(player_local)
            try:
                for p_id, player in player_vbcable.items():
                    try:
                        player.stop()
                        player.release()
                        # del player_vbcable[p_id]
                    except Exception as e:
                        pass

                for p_id, player in player_local.items():
                    try:
                        player.stop()
                        player.release()
                        # del player_local[p_id]
                    except Exception as e:
                        pass
                break
            except RuntimeError as e:
                print("RT error:", e)
                ...
            
        player_vbcable.clear()
        player_local.clear()
        return jsonify({"success": True})
    
    
def remove_player(sb_type, p_id):
    global player_vbcable, player_local
    try:
        if sb_type == 1:
            del player_vbcable[p_id]
        elif sb_type == 2:
            del player_local[p_id]
        else:
            del p_id
    except KeyError:
        pass
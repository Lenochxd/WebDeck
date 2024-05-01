try: import vlc
except: pass
from flask import jsonify

from app.functions.load_config import load_config
from app.functions.load_lang_file import load_lang_file

from app.buttons.soundboard.devices import get_device
from app.buttons.soundboard.ffmpeg import silence_path


config = load_config()
text = load_lang_file(config["settings"]["language"])
cable_input_device = get_device(config["settings"]["soundboard"]["vbcable"])
vlc_installed = cable_input_device != "ERROR_NO_VLC"

player_vbcable = {}
player_ear_soundboard = {}


def playsound(file_path: str, sound_volume, ear_soundboard=True):
    global cable_input_device, player
    if not vlc_installed:
        print("VLC is not installed!")
        return jsonify({"success": False, "message": text["vlc_not_installed_error"]})
    else:
        if config["settings"]["fix-stop-soundboard"] == "true":
            file_path = silence_path(file_path)
            if file_path == False:
                return jsonify({"success": False, "message": text["ffmpeg_not_installed_error"]})
        print(f"Play: {file_path}  -  volume:{sound_volume}\r\n")
        print(len(player_vbcable))
        print(player_vbcable)

        p_id = len(player_vbcable.keys())
        if p_id <= 3:
            player_vbcable[p_id] = vlc.MediaPlayer(file_path)
            player_vbcable[p_id].audio_set_volume(int(sound_volume * 100))
            player_vbcable[p_id].audio_output_device_set(None, cable_input_device)
            player_vbcable[p_id].play()
            player_vbcable[p_id].event_manager().event_attach(
                vlc.EventType.MediaPlayerEndReached, lambda x: remove_player(1, p_id)
            )

            if ear_soundboard:
                player_ear_soundboard[p_id] = vlc.MediaPlayer(file_path)
                player_ear_soundboard[p_id].audio_set_volume(int(sound_volume * 100))
                player_ear_soundboard[p_id].play()
                player_ear_soundboard[p_id].event_manager().event_attach(
                    vlc.EventType.MediaPlayerEndReached,
                    lambda x: remove_player(2, p_id),
                )

        else:
            player_vbcable[0].stop()
            player_vbcable[0].set_time(0)
            player_vbcable[0].play()
            player_vbcable[0].event_manager().event_attach(
                vlc.EventType.MediaPlayerEndReached, lambda x: remove_player(1, p_id)
            )

            if ear_soundboard:
                player_ear_soundboard[0].stop()
                player_ear_soundboard[0].set_time(0)
                player_ear_soundboard[0].play()
                player_ear_soundboard[0].event_manager().event_attach(
                    vlc.EventType.MediaPlayerEndReached,
                    lambda x: remove_player(2, p_id),
                )
        return jsonify({"success": True})
    

def stopsound():
    if not vlc_installed:
        print("VLC is not installed!")
        return jsonify({"success": False, "message": text["vlc_not_installed_error"]})
    else:
        global player_vbcable, player_ear_soundboard
        
        try:
            last_key = list(player_vbcable.keys())[-1]
            last_value = player_vbcable[last_key]
        except IndexError:
            return jsonify({"success": True, "message": "There are no sounds actually playing"})
        
        while str(last_value.get_state()) == "State.Playing":
            print(player_vbcable)
            print(player_ear_soundboard)
            try:
                for p_id, player in player_vbcable.items():
                    try:
                        player.stop()
                        player.release()
                        # del player_vbcable[p_id]
                    except Exception as e:
                        pass

                for p_id, player in player_ear_soundboard.items():
                    try:
                        player.stop()
                        player.release()
                        # del player_ear_soundboard[p_id]
                    except Exception as e:
                        pass
                break
            except RuntimeError as e:
                print("RT error:", e)
                ...
            
        player_vbcable.clear()
        player_ear_soundboard.clear()
        return jsonify({"success": True})
    
    
def remove_player(sb_type, p_id):
    global player_vbcable, player_ear_soundboard
    try:
        if sb_type == 1:
            del player_vbcable[p_id]
        elif sb_type == 2:
            del player_ear_soundboard[p_id]
        else:
            del p_id
    except KeyError:
        pass
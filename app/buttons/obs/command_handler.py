from obswebsocket import obsws
from obswebsocket import requests as obsrequests

from app.utils.global_variables import get_global_variables
from app.utils.languages import text
from app.utils.logger import log

import app.buttons.obs.scenes as scene
import app.buttons.obs.recording as recording
import app.buttons.obs.streaming as stream
import app.buttons.obs.virtualcam as virtualcam


#    https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md
#    https://github.com/Elektordi/obs-websocket-py



def handle_command(message):
    try:
        obs_host, obs_port, obs_password = get_global_variables(("obs_host", "obs_port", "obs_password"))
        
        obs = obsws(obs_host, obs_port, obs_password)
        obs.connect()
    except Exception as e:
        if "10061" in str(e):
            log.exception(e, "Failed connection to obs: The websocket server cannot be found.", log_traceback=False)
            error = text("obs_error_10061")
        elif "password may be inco" in str(e):
            log.exception(e, "Failed connection to obs: Password may be incorrect.", log_traceback=False)
            error = text("obs_error_incorrect_password")
        else:
            error = str(e)

        raise ConnectionError(f"{text('obs_failed_connection_error').replace('.','')}: {error}")


    if message.startswith("/obs_toggle_rec"):
        recording.toggle(obs)

    elif message.startswith("/obs_start_rec"):
        recording.start(obs)

    elif message.startswith("/obs_stop_rec"):
        recording.stop(obs)


    elif message.startswith("/obs_toggle_rec_pause"):
        recording.pause_toggle(obs)

    elif message.startswith("/obs_pause_rec"):
        recording.pause(obs)
        
    elif message.startswith("/obs_resume_rec"):
        recording.resume(obs)


    elif message.startswith("/obs_toggle_stream"):
        stream.toggle(obs)

    elif message.startswith("/obs_start_stream"):
        stream.start(obs)

    elif message.startswith("/obs_stop_stream"):
        stream.stop(obs)


    elif message.startswith("/obs_toggle_virtualcam"):
        virtualcam.toggle(obs)

    elif message.startswith("/obs_start_virtualcam"):
        virtualcam.start(obs)

    elif message.startswith("/obs_stop_virtualcam"):
        virtualcam.stop(obs)


    elif message.startswith("/obs_scene"):
        scene_name = message.replace("/obs_scene", "")
        scene.set(obs, scene_name)
    
    
    elif message.startswith("/obs_key"):
        hotkey = message.split(' ')[-1]
        result = obs.call(obsrequests.TriggerHotkeyByKeySequence(keyId="OBS_KEY_"+hotkey))
        if "failed" in str(result):
            log.error(f"Failed to trigger hotkey '{hotkey}': {result}")
            raise RuntimeError(f"{text('failed')} :/")
        log.success(f"Hotkey triggered '{hotkey}' successfully.")


    obs.disconnect()
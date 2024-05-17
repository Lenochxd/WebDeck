from obswebsocket import obsws, events
from obswebsocket import requests as obsrequests

from flask import jsonify

from app.functions.global_variables import set_global_variable, get_global_variable, get_global_variables

import app.buttons.obs.scenes as scene
import app.buttons.obs.recording as recording
import app.buttons.obs.streaming as stream
import app.buttons.obs.virtualcam as virtualcam


#    https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md
#    https://github.com/Elektordi/obs-websocket-py


def reload_obs():
    # Set up the OBS WebSocket client
    config = get_global_variable("config")
    obs_host = config["settings"]["obs"]["host"]
    obs_port = int(config["settings"]["obs"]["port"])
    obs_password = config["settings"]["obs"]["password"]

    obs = obsws(obs_host, obs_port, obs_password)
    
    set_global_variable("obs_host", obs_host)
    set_global_variable("obs_port", obs_port)
    set_global_variable("obs_password", obs_password)

    return obs_host, obs_port, obs_password, obs

obs_host, obs_port, obs_password, obs = reload_obs()


def handle_command(message, text):
    try:
        obs_host, obs_port, obs_password = get_global_variables(("obs_host", "obs_port", "obs_password"))
        
        obs = obsws(obs_host, obs_port, obs_password)
        obs.connect()
    except Exception as e:
        if "10061" in str(e):
            e = text["obs_error_10061"]
        elif "password may be inco" in str(e):
            e = text["obs_error_incorrect_password"]

        return jsonify({
            "success": False,
            "message": f"{text['obs_failed_connection_error'].replace('.','')}: {e}",
        })


    if message.startswith("/obs_toggle_rec"):
        recording.toggle(obs, text)

    elif message.startswith("/obs_start_rec"):
        recording.start(obs, text)

    elif message.startswith("/obs_stop_rec"):
        recording.stop(obs, text)


    elif message.startswith("/obs_toggle_rec_pause"):
        recording.pause_toggle(obs, text)

    elif message.startswith("/obs_pause_rec"):
        recording.pause(obs, text)
        
    elif message.startswith("/obs_resume_rec"):
        recording.resume(obs, text)


    elif message.startswith("/obs_toggle_stream"):
        stream.toggle(obs, text)

    elif message.startswith("/obs_start_stream"):
        stream.start(obs, text)

    elif message.startswith("/obs_stop_stream"):
        stream.stop(obs, text)


    elif message.startswith("/obs_toggle_virtualcam"):
        virtualcam.toggle(obs, text)

    elif message.startswith("/obs_start_virtualcam"):
        virtualcam.start(obs, text)

    elif message.startswith("/obs_stop_virtualcam"):
        virtualcam.stop(obs, text)


    elif message.startswith("/obs_scene"):
        scene_name = message.replace("/obs_scene", "")
        scene.set(obs, scene_name)


    obs.disconnect()
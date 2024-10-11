from obswebsocket import requests as obsrequests
from flask import jsonify
from app.utils.languages import text


def toggle(obs):
    result = obs.call(obsrequests.ToggleStream())
    print("Streaming toggled successfully.")
    if "failed" in str(result):
        return jsonify({"success": False, "message": f"{text('failed')} :/"})

def start(obs):
    recording_status = obs.call(obsrequests.GetStreamStatus())
    if recording_status.getOutputActive():
        print("OBS is already streaming.")
        return jsonify({"success": False, "message": text("obs_already_streaming")})
    else:
        obs.call(obsrequests.StartStream())
        print("Stream started successfully.")

def stop(obs):
    recording_status = obs.call(obsrequests.GetStreamStatus())
    if recording_status.getOutputActive():
        obs.call(obsrequests.StopStream())
        print("Stream stopped successfully.")
    else:
        print("OBS is not streaming.")
        return jsonify({"success": False, "message": text("obs_not_streaming")})
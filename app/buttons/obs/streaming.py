from obswebsocket import requests as obsrequests
from flask import jsonify
from app.utils.languages import text


def toggle(obs):
    result = obs.call(obsrequests.ToggleStream())
    print("Streaming toggled successfully.")
    if "failed" in str(result):
        raise RuntimeError(f"{text('failed')} :/")

def start(obs):
    recording_status = obs.call(obsrequests.GetStreamStatus())
    if recording_status.getOutputActive():
        print("OBS is already streaming.")
        raise RuntimeError(f"{text('obs_already_streaming')} :/")
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
        raise RuntimeError(f"{text('obs_not_streaming')} :/")
from obswebsocket import requests as obsrequests
from flask import jsonify
from app.utils.languages import text

def toggle(obs):
    result = obs.call(obsrequests.ToggleRecord())
    print("Recording toggled successfully.")
    if "failed" in str(result):
        raise RuntimeError(f"{text('failed')} :/")

def start(obs):
    recording_status = obs.call(obsrequests.GetRecordStatus())
    if recording_status.getOutputActive():
        print("OBS is already recording.")
        raise RuntimeError(f"{text('obs_already_recording')}")
    else:
        obs.call(obsrequests.StartRecord())
        print("Recording started successfully.")

def stop(obs):
    recording_status = obs.call(obsrequests.GetRecordStatus())
    if recording_status.getOutputActive():
        obs.call(obsrequests.StopRecord())
        print("Recording stopped successfully.")
    else:
        print("OBS is not recording.")
        raise RuntimeError(f"{text('obs_not_recording')}")


def pause_toggle(obs):
    result = obs.call(obsrequests.ToggleRecordPause())
    print("Play/pause toggled successfully.")
    if "failed" in str(result):
        raise RuntimeError(f"{text('failed')} :/")
    
def pause(obs):
    recording_status = obs.call(obsrequests.GetRecordStatus())
    if not recording_status.getOutputActive():
        raise RuntimeError(f"{text('obs_no_recording_can_be_paused')}")

    result = obs.call(obsrequests.PauseRecord())
    if "failed" in str(result):
        raise RuntimeError(f"{text('obs_no_recording_can_be_paused')}")

def resume(obs):
    result = obs.call(obsrequests.ResumeRecord())
    if "failed" in str(result):
        raise RuntimeError(f"{text('obs_no_recording_is_paused')}")
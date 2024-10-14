from obswebsocket import requests as obsrequests
from flask import jsonify
from app.utils.languages import text


def toggle(obs):
    result = obs.call(obsrequests.ToggleVirtualCam())
    print("Virtual cam toggled successfully.")
    if "failed" in str(result):
        raise RuntimeError(f"{text('failed')} :/")

def start(obs):
    recording_status = obs.call(obsrequests.GetVirtualCamStatus())
    print("obs recording_status: ", recording_status)
    if recording_status.getOutputActive():
        print("Virtual cam is already started.")
        raise RuntimeError(f"{text('obs_already_vcam')} :/")
    else:
        obs.call(obsrequests.StartVirtualCam())
        print("Virtual cam started successfully.")

def stop(obs):
    recording_status = obs.call(obsrequests.GetVirtualCamStatus())
    if recording_status.getOutputActive():
        obs.call(obsrequests.StopVirtualCam())
        print("Virtual cam stopped successfully.")
    else:
        print("Virtual cam is already stopped.")
        raise RuntimeError(f"{text('obs_no_vcam')} :/")
from obswebsocket import requests as obsrequests
from app.utils.languages import text
from app.utils.logger import log


def toggle(obs):
    result = obs.call(obsrequests.ToggleVirtualCam())
    log.success("Virtual cam toggled successfully.")
    if "failed" in str(result):
        log.error(f"Failed to toggle virtual cam: {result}")
        raise RuntimeError(f"{text('failed')} :/")

def start(obs):
    recording_status = obs.call(obsrequests.GetVirtualCamStatus())
    log.debug("obs recording_status: ", recording_status)
    if recording_status.getOutputActive():
        log.notice("Virtual cam is already started.")
        raise RuntimeError(f"{text('obs_already_vcam')} :/")
    else:
        obs.call(obsrequests.StartVirtualCam())
        log.success("Virtual cam started successfully.")

def stop(obs):
    recording_status = obs.call(obsrequests.GetVirtualCamStatus())
    if recording_status.getOutputActive():
        obs.call(obsrequests.StopVirtualCam())
        log.success("Virtual cam stopped successfully.")
    else:
        log.notice("Virtual cam is already stopped.")
        raise RuntimeError(f"{text('obs_no_vcam')} :/")
from obswebsocket import requests as obsrequests
from app.utils.languages import text
from app.utils.logger import log

def toggle(obs):
    result = obs.call(obsrequests.ToggleStream())
    log.success("Streaming toggled successfully.")
    if "failed" in str(result):
        log.error(f"Failed to toggle streaming: {result}")
        raise RuntimeError(f"{text('failed')} :/")

def start(obs):
    recording_status = obs.call(obsrequests.GetStreamStatus())
    if recording_status.getOutputActive():
        log.notice("OBS is already streaming.")
        raise RuntimeError(f"{text('obs_already_streaming')} :/")
    else:
        obs.call(obsrequests.StartStream())
        log.success("Stream started successfully.")

def stop(obs):
    recording_status = obs.call(obsrequests.GetStreamStatus())
    if recording_status.getOutputActive():
        obs.call(obsrequests.StopStream())
        log.success("Stream stopped successfully.")
    else:
        log.notice("OBS is not streaming.")
        raise RuntimeError(f"{text('obs_not_streaming')} :/")
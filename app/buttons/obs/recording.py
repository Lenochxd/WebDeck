from obswebsocket import requests as obsrequests
from app.utils.languages import text
from app.utils.logger import log


def toggle(obs):
    result = obs.call(obsrequests.ToggleRecord())
    log.success("Recording toggled successfully.")
    if "failed" in str(result):
        log.error(f"Failed to toggle recording: {result}")
        raise RuntimeError(f"{text('failed')} :/")

def start(obs):
    recording_status = obs.call(obsrequests.GetRecordStatus())
    if recording_status.getOutputActive():
        log.notice("OBS is already recording.")
        raise RuntimeError(f"{text('obs_already_recording')}")
    else:
        obs.call(obsrequests.StartRecord())
        log.success("Recording started successfully.")

def stop(obs):
    recording_status = obs.call(obsrequests.GetRecordStatus())
    if recording_status.getOutputActive():
        obs.call(obsrequests.StopRecord())
        log.success("Recording stopped successfully.")
    else:
        log.notice("OBS is not recording.")
        raise RuntimeError(f"{text('obs_not_recording')}")


def pause_toggle(obs):
    result = obs.call(obsrequests.ToggleRecordPause())
    log.success("Play/pause toggled successfully.")
    if "failed" in str(result):
        log.error(f"Failed to toggle play/pause: {result}")
        raise RuntimeError(f"{text('failed')} :/")
    
def pause(obs):
    recording_status = obs.call(obsrequests.GetRecordStatus())
    if not recording_status.getOutputActive():
        log.notice("OBS is not recording, cannot pause.")
        raise RuntimeError(f"{text('obs_no_recording_can_be_paused')}")

    result = obs.call(obsrequests.PauseRecord())
    if "failed" in str(result):
        log.error(f"Failed to pause recording. It might be that the recording is already paused or no recording is currently active. Details: {result}")
        raise RuntimeError(f"{text('obs_no_recording_can_be_paused')}")

def resume(obs):
    # TODO: Ensure consistency with the pause() function by checking if OBS is recording before attempting to resume
    result = obs.call(obsrequests.ResumeRecord())
    if "failed" in str(result):
        log.error(f"Failed to unpause recording. It might be that the recording is already active or no recording is currently active and paused. Details: {result}")
        raise RuntimeError(f"{text('obs_no_recording_is_paused')}")
from app.utils.languages import text
from app.utils.logger import log

def manage(sp, message):
    # Get the current playback information
    playback_info = sp.current_playback()

    # Check if there is an active device
    if playback_info and playback_info["is_playing"] and playback_info["device"]:
        device_id = playback_info["device"]["id"]
    else:
        log.warning("No active devices on Spotify found.")
        raise RuntimeError(text("spotify_no_active_device_error"))

    # Get the current volume
    current_volume = playback_info["device"]["volume_percent"]
    log.debug(f"Current spotify volume: {current_volume}")

    if "-" in message:
        try:
            target_volume = current_volume - int(message.replace("/spotify volume -", ""))
        except ValueError:
            target_volume = current_volume - 10
    elif "+" in message:
        try:
            target_volume = current_volume + int(message.replace("/spotify volume +", ""))
        except ValueError:
            target_volume = current_volume + 10
    elif "set" in message:
        target_volume = int(message.replace("/spotify volume set", ""))

    target_volume = max(0, min(100, target_volume))
    try:
        sp.volume(target_volume, device_id=device_id)
    except Exception as e:
        if "premium" in str(e).lower():
            log.exception(e, "Unable to apply volume because Spotify Prenium is required.")
            raise Exception(f"{text('spotify_volume_prenium_error')}")
        else:
            log.exception(e, message="Error while setting the spotify volume.")
            raise Exception(f"{text('spotify_apply_volume_error')}: {e}")

    # Get the updated volume
    playback_info = sp.current_playback()
    current_volume = playback_info["device"]["volume_percent"]
    log.debug(f"Updated spotify volume: {current_volume}")
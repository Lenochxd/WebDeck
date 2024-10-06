def manage(sp, message, text):
    # Get the current playback information
    playback_info = sp.current_playback()

    # Check if there is an active device
    if playback_info and playback_info["is_playing"] and playback_info["device"]:
        device_id = playback_info["device"]["id"]
    else:
        print("No active devices on Spotify found.")
        return

    # Get the current volume
    current_volume = playback_info["device"]["volume_percent"]
    print(f"Current volume: {current_volume}")

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
        try:
            target_volume = int(message.replace("/spotify volume set", ""))
        except Exception as e:
            print(f"{text['spotify_apply_volume_error']}: {e}")
            return

    target_volume = max(0, min(100, target_volume))
    try:
        sp.volume(target_volume, device_id=device_id)
    except Exception as e:
        print(f"{text['spotify_volume_prenium_error']}: {e}")
        return

    # Get the updated volume
    playback_info = sp.current_playback()
    current_volume = playback_info["device"]["volume_percent"]
    print(f"Updated volume: {current_volume}")
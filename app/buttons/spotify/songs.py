from app.utils.logger import log


def save(sp):
    # Get information about the user's currently playing track
    track_info = sp.current_playback()

    # If a track is currently playing, save/unsave the track
    if track_info is not None:
        track_id = track_info["item"]["id"]

        is_saved = sp.current_user_saved_tracks_contains(tracks=[track_id])[0]
        if is_saved:
            sp.current_user_saved_tracks_delete(tracks=[track_id])
            log.success(f"Removed track {track_info['item']['name']} by {track_info['item']['artists'][0]['name']} from saved tracks")
        else:
            sp.current_user_saved_tracks_add(tracks=[track_id])
            log.success(f"Saved track {track_info['item']['name']} by {track_info['item']['artists'][0]['name']}")
    else:
        log.warning("No track currently playing.")
        raise RuntimeError("spotify_no_track_playing_error")
        
        
def play(sp, song_name):
    results = sp.search(song_name, 1, 0, "track")
    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        sp.start_playback(uris=[track_uri])
    else:
        log.error(f"No track found for '{song_name}'")
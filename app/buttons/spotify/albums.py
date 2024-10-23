from app.utils.logger import log


def save(sp):
    # Get information about the user's currently playing track
    track_info = sp.current_playback()

    # If a track is currently playing, save/unsave the album
    if track_info is not None:
        album_id = track_info["item"]["album"]["id"]

        is_saved = sp.current_user_saved_albums_contains(albums=[album_id])[0]
        if is_saved:
            sp.current_user_saved_albums_delete(albums=[album_id])
            log.info(f"Removed album '{track_info['item']['album']['name']}' by {', '.join(artist['name'] for artist in track_info['item']['album']['artists'])} from saved albums")
        else:
            sp.current_user_saved_albums_add(albums=[album_id])
            log.info(f"Saved album '{track_info['item']['album']['name']}' by {', '.join(artist['name'] for artist in track_info['item']['album']['artists'])}")
    else:
        log.notice("No album currently playing.")
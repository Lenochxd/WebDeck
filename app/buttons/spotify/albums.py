def save(sp):
    # Get information about the user's currently playing track
    track_info = sp.current_playback()

    # If a track is currently playing, save/unsave the album
    if track_info is not None:
        album_id = track_info["item"]["album"]["id"]

        is_saved = sp.current_user_saved_albums_contains(albums=[album_id])[0]
        if is_saved:
            sp.current_user_saved_albums_delete(albums=[album_id])
            print(f"Removed album {track_info['item']['album']['name']} by {track_info['item']['album']['artists'][0]['name']}")
        else:
            sp.current_user_saved_albums_add(albums=[album_id])
            print(f"saved album {track_info['item']['album']['name']} by {track_info['item']['album']['artists'][0]['name']}")
    else:
        print("No album currently playing.")
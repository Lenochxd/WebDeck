from app.functions.show_error import show_error


def play(sp, playlist_name):
    playlists = sp.current_user_playlists()  # Retrieve current user's playlists

    for playlist in playlists["items"]:
        if playlist_name.lower().strip() in playlist["name"].lower().strip():
            playlist_uri = playlist["uri"]
            sp.start_playback(context_uri=playlist_uri)
            break
    else:
        print(f"Playlist '{playlist_name}' not found.")
        
        
def manage(sp, message, playlist_name):
    playlists = sp.current_user_playlists()
    playlist_id = next((playlist["id"] for playlist in playlists["items"] if playlist["name"] == playlist_name), None)

    if playlist_id is None:
        show_error(f"Playlist named '{playlist_name}' not found.")
    else:
        playback = sp.current_playback()
        track_id = playback["item"]["id"]
        track_uri = playback["item"]["uri"]
        
        if "add_or_remove" in message or "toggle" in message:
            playlist_items = sp.playlist_items(playlist_id, fields="items(track(uri))")
            track_uris = [item["track"]["uri"] for item in playlist_items["items"]]

            if track_uri in track_uris:
                sp.playlist_remove_all_occurrences_of_items(playlist_id, [track_uri])
                print("The track has been removed from the playlist.")
            else:
                sp.playlist_add_items(playlist_id, [track_id])
                print("The track has been added to the playlist.")
                
        elif "add_to_playlist" in message:
            sp.playlist_add_items(playlist_id, [track_id])
            
        elif "remove_from_playlist" in message:
            sp.playlist_remove_all_occurrences_of_items(playlist_id, [track_uri])
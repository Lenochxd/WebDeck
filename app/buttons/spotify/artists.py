from flask import jsonify
from app.utils.languages import text
from app.utils.logger import log


def manage(sp, message):
    playback = sp.current_playback()
    artist_id = playback["item"]["artists"][0]["id"]
    artist_name = playback["item"]["artists"][0]["name"]
    
    if "follow_or_unfollow_artist" in message or "toggle_follow" in message:
        results = sp.search(q=artist_name, type="artist")
        items = results["artists"]["items"]
        if items:
            artist_id = items[0]["id"]
        else:
            log.error(f"Unable to find artist '{artist_name}' on Spotify.")

        # Check if the user is subscribed to the corresponding artist
        is_following = sp.current_user_following_artists(ids=[artist_id])[0]
        if is_following:
            log.debug(f"The user is subscribed to the artist '{artist_name}'.")
            sp.user_unfollow_artists([artist_id])
            log.success("The artist has been removed from the subscription list.")
            return jsonify({"success" : True, "message": text("spotify_unfollow_artist_success").replace('%artist_name%', artist_name)})
        else:
            log.debug(f"The user is not subscribed to the artist '{artist_name}'.")
            sp.user_follow_artists([artist_id])
            log.success("The artist has been added to the subscription list.")
            return jsonify({"success" : True, "message": text("spotify_unfollow_artist_success").replace('%artist_name%', artist_name)})

    elif "unfollow_artist" in message:
        sp.user_unfollow_artists([artist_id])
        log.success("The artist has been removed from the subscription list.")
        return jsonify({"success" : True, "message": text("spotify_unfollow_artist_success").replace('%artist_name%', artist_name)})
        
    elif "follow_artist" in message:
        sp.user_follow_artists([artist_id])
        log.success("The artist has been added to the subscription list.")
        return jsonify({"success" : True, "message": text("spotify_unfollow_artist_success").replace('%artist_name%', artist_name)})
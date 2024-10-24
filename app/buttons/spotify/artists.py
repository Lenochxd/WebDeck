from flask import jsonify
from app.utils.languages import text
from app.utils.logger import log


def manage(sp, message):
    playback = sp.current_playback()
    artist = playback["item"]["artists"][0]
    artist_id = artist["id"]
    artist_name = artist["name"]

    def follow_artist():
        sp.user_follow_artists([artist_id])
        log.success("The artist has been added to the subscription list.")
        return jsonify({"success": True, "message": text("spotify_follow_artist_success").replace('%artist_name%', artist_name)})

    def unfollow_artist():
        sp.user_unfollow_artists([artist_id])
        log.success("The artist has been removed from the subscription list.")
        return jsonify({"success": True, "message": text("spotify_unfollow_artist_success").replace('%artist_name%', artist_name)})

    if "follow_or_unfollow_artist" in message or "toggle_follow" in message:
        is_following = sp.current_user_following_artists(ids=[artist_id])[0]
        if is_following:
            log.debug(f"The user is subscribed to the artist '{artist_name}'.")
            return unfollow_artist()
        else:
            log.debug(f"The user is not subscribed to the artist '{artist_name}'.")
            return follow_artist()

    elif "unfollow_artist" in message:
        return unfollow_artist()

    elif "follow_artist" in message:
        return follow_artist()

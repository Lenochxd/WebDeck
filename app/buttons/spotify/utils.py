import spotipy.util as util
import json
from app.utils.logger import log


def initialize():
    # Reload config before assuming it's not set
    with open('.config/config.json', encoding= "utf-8") as f:
        config = json.load(f)

    # Check if client id and client secret are set in the config
    if not config["settings"]["spotify_api"].get("client_id") or not config["settings"]["spotify_api"].get("client_secret"):
        log.warning("Spotify client ID and/or client secret not set in the config.")
        return None

    # Set up the Spotify API client
    try:
        spotify_redirect_uri = "http://localhost:8888/callback"
        spotify_scope = "user-library-modify user-library-read user-read-currently-playing user-read-playback-state user-modify-playback-state playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-follow-modify user-follow-read"
        return util.prompt_for_user_token(
            config["settings"]["spotify_api"]["username"],
            spotify_scope,
            config["settings"]["spotify_api"]["client_id"],
            config["settings"]["spotify_api"]["client_secret"],
            spotify_redirect_uri,
        )
    except Exception as e:
        log.exception(e, "Failed to start spotipy")

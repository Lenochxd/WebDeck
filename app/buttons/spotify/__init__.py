import spotipy
import spotipy.util as util
import json

with open('config.json', encoding= "utf-8") as f:
    config = json.load(f)
    
def initialize():
    # Set up the Spotify API client
    try:
        spotify_redirect_uri = "http://localhost:8888/callback"
        spotify_scope = "user-library-modify user-library-read user-read-currently-playing user-read-playback-state user-modify-playback-state playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-follow-modify user-follow-read"
        return util.prompt_for_user_token(
            config["settings"]["spotify-api"]["USERNAME"],
            spotify_scope,
            config["settings"]["spotify-api"]["CLIENT_ID"],
            config["settings"]["spotify-api"]["CLIENT_SECRET"],
            spotify_redirect_uri,
        )
    except Exception as e:
        print(f'ERROR: Failed to start spotipy, {e}')
        
import spotipy
import spotipy.util as util
import json

import app.buttons.spotify.albums as album
import app.buttons.spotify.songs as song
import app.buttons.spotify.playlists as playlist
import app.buttons.spotify.artists as artist
import app.buttons.spotify.volume as volume


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

spotify_token = initialize()


def handle_command(message, text):
    sp = spotipy.Spotify(auth=spotify_token)

    if message.startswith(("/spotify savesong", "/spotify likesong")):
        song.save(sp)

    elif message.startswith(("/spotify savealbum", "/spotify likealbum")):
        album.save(sp)

    elif message.startswith("/spotify playsong"):
        song_name = message.replace("/spotify playsong", "").strip()
        song.play(sp, song_name)

    elif message.startswith("/spotify playplaylist"):
        playlist_name = message.replace("/spotify playplaylist", "").strip()
        playlist.play(sp, playlist_name)

    elif message.startswith(("/spotify add_to_playlist", "/spotify remove_from_playlist", "/spotify add_or_remove")):
        playlist_name = message.replace("/spotify add_to_playlist", "").replace("/spotify remove_from_playlist", "").replace("/spotify add_or_remove", "").strip()
        playlist.manage(sp, message, playlist_name)

    elif message.startswith(("/spotify follow_artist", "/spotify unfollow_artist", "/spotify follow_or_unfollow_artist")):
        artist.manage(sp, message)

    elif message.startswith(("/spotify volume +", "/spotify volume -", "/spotify volume set")):
        volume.manage(sp, text, message)
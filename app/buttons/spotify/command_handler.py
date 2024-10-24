import spotipy
from app.utils.languages import text
from app.utils.logger import log

import app.buttons.spotify.albums as album
import app.buttons.spotify.songs as song
import app.buttons.spotify.playlists as playlist
import app.buttons.spotify.artists as artist
import app.buttons.spotify.volume as volume
from .utils import initialize

spotify_token = ''


def handle_command(message):
    global spotify_token

    if not spotify_token:
        spotify_token = initialize()
        if not spotify_token:
            log.error("Spotify not initialized, check if your credentials are correct.")
            raise RuntimeError(text("spotify_not_initialized"))
    
    sp = spotipy.Spotify(auth=spotify_token)

    if message.startswith(("/spotify savesong", "/spotify likesong")):
        return song.save(sp)

    elif message.startswith(("/spotify savealbum", "/spotify likealbum")):
        return album.save(sp)

    elif message.startswith("/spotify playsong"):
        song_name = message.replace("/spotify playsong", "").strip()
        return song.play(sp, song_name)

    elif message.startswith("/spotify playplaylist"):
        playlist_name = message.replace("/spotify playplaylist", "").strip()
        return playlist.play(sp, playlist_name)

    elif message.startswith(("/spotify add_to_playlist", "/spotify remove_from_playlist", "/spotify add_or_remove")):
        playlist_name = message.replace("/spotify add_to_playlist", "").replace("/spotify remove_from_playlist", "").replace("/spotify add_or_remove", "").strip()
        return playlist.manage(sp, message, playlist_name)

    elif message.startswith(("/spotify follow_artist", "/spotify unfollow_artist", "/spotify follow_or_unfollow_artist")):
        return artist.manage(sp, message)

    elif message.startswith(("/spotify volume +", "/spotify volume -", "/spotify volume set")):
        volume.manage(sp, message)
import spotipy
import json
from flask import jsonify

import app.buttons.spotify.albums as album
import app.buttons.spotify.songs as song
import app.buttons.spotify.playlists as playlist
import app.buttons.spotify.artists as artist
import app.buttons.spotify.volume as volume

from .utils import initialize
spotify_token = initialize()


def handle_command(message):
    global spotify_token

    if not spotify_token:
        spotify_token = initialize()
        if not spotify_token:
            raise Exception("Spotify token is not initialized.")
    
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
        volume.manage(sp, message)
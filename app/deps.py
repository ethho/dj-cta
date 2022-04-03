import os
import requests
from random import randint
from fastapi import Depends
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

AUTH_URL = 'https://accounts.spotify.com/api/token'
SPT_SECRET = os.environ['SPT_SECRET']
SPT_CLIENT_ID = os.environ['SPT_CLIENT_ID']


def get_sp():
    auth_manager = SpotifyClientCredentials(client_id=SPT_CLIENT_ID, client_secret=SPT_SECRET)
    return spotipy.Spotify(auth_manager=auth_manager)

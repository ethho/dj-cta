import os
import requests
from random import randint
from fastapi import Depends
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

AUTH_URL = 'https://accounts.spotify.com/api/token'
SPT_SECRET = os.environ['SPT_SECRET']
SPT_CLIENT_ID = os.environ['SPT_CLIENT_ID']


def get_spt_access_token():
    resp = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': SPT_CLIENT_ID,
        'client_secret': SPT_SECRET,
    })
    return resp.json()['access_token']


def get_random_words(n: int = 2):
    # r.get_random_words(hasDictionaryDef="true", includePartOfSpeech="noun,verb", minCorpusCount=1, maxCorpusCount=10, minDictionaryCount=1, maxDictionaryCount=10, minLength=5, maxLength=10, sortBy="alpha", sortOrder="asc", limit=15)
    # words = RandomWords().get_random_words(
    #     limit=2, 
    #     minDictionaryCount=6, 
    #     maxDictionaryCount=50
    # )
    with open('./app/common-words.txt', 'r') as f:
        words = [w.strip() for w in f.readlines()]
    if not words or bool(os.environ.get("APRIL_FOOLS", "0") == "1"):
        return ['never', 'gonna', 'give', 'you', 'up'] 
    return [words[randint(0, 4999)] for _ in range(n)]
    

def get_random_query(query_len: int = 3):
    alph = 'abcdefghijklmnopqrstuvwxyz'
    rchars = "".join(alph[randint(0, len(alph))] for _ in range(query_len))
    return "%" + "".join(rchars) + "%"

# function getRandomSearch() {
#   // A list of all characters that can be chosen.
#   const characters = 'abcdefghijklmnopqrstuvwxyz';
  
#   // Gets a random character from the characters string.
#   const randomCharacter = characters.charAt(Math.floor(Math.random() * characters.length));
#   let randomSearch = '';

#   // Places the wildcard character at the beginning, or both beginning and end, randomly.
#   switch (Math.round(Math.random())) {
#     case 0:
#       randomSearch = randomCharacter + '%';
#       break;
#     case 1:
#       randomSearch = '%' + randomCharacter + '%';
#       break;
#   }

#   return randomSearch;
# }


def get_sp():
    auth_manager = SpotifyClientCredentials(client_id=SPT_CLIENT_ID, client_secret=SPT_SECRET)
    return spotipy.Spotify(auth_manager=auth_manager)


def get_rand_pl(sp = Depends(get_sp), max_iters: int = 20):
    '''
    Short songs
    https://open.spotify.com/playlist/5XnkjnyMyg2ZRPBCYVHkbw?si=f9cc5340dd7645eb
    '''
    playlists = sp.user_playlists('spotify')
    i = 0
    while playlists:
        if i == randint(0, max_iters):
            break
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            break
        i += 1
    pl = playlists['items']
    return pl[randint(0, len(pl))]


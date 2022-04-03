import os
import requests
# from random_word import RandomWords
from random import randint

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
    return [words[randint(0, 5000)] for _ in range(n)]
    

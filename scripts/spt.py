import os
from random import randint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import logging
logging.basicConfig(level=logging.INFO)

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

'''
playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
    break
foo = playlists['items'][0]
tr = sp.playlist_items('spotify:playlist:37i9dQZF1DZ06evO4nBpII', limit=10, offset=5)['items'][0]
tr['track']['external_urls']['spotify']
breakpoint()
'''

def main(playlist_uris):
    # TODO: get duration
    stopdur = 180

    # Choose a song
    chosen = None
    trs = list()
    for pl in playlist_uris:

        tracks = sp.playlist_items(pl, limit=50, offset=randint(0, 10))['items']
        trs.extend(foo)
    trs = (
        
    )

    for pl in pls:
        for tr in pl:
            trdur = int(tr['track']['duration_ms']) / 1000.
            if abs(trdur - stopdur) < SEC_THRESH:
                chosen = tr['track']['external_urls']['spotify']
                break
        if chosen:
            break

    if not chosen or bool(os.environ.get("APRIL_FOOLS", "0") == "1"):
        # chosen = "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT?si=c0637df83ee748fe"
        # TODO
        chosen = "no track found"
    print({'url': chosen})


def get_rand_pl(max_iters: int = 20):
    '''
    Short songs
    https://open.spotify.com/playlist/5XnkjnyMyg2ZRPBCYVHkbw?si=f9cc5340dd7645eb
    '''
    playlists = sp.user_playlists('spotify', limit=50)
    while playlists:
        for pl in playlists['items']:
            yield pl['uri']
        if i == randint(0, max_iters):
            break
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            break


if __name__ == '__main__':
    pls = get_rand_pl()
    main(pls)
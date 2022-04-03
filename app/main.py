import os
from typing import Optional
from random import randint
import requests
from fastapi import Depends, FastAPI, APIRouter
from pydantic import BaseModel
from .deps import get_sp

SEC_THRESH = 15
DEBUG = bool(os.environ.get('DEBUG', '0') == '1')
app = FastAPI(debug=DEBUG)

# ---------------------------- Models ------------------------------------------

class LocModel(BaseModel):
    stopid: int
    # description: Optional[str] = None
    # price: float
    # tax: Optional[float] = None

# ---------------------------- Routes ------------------------------------------

@app.get("/")
async def song_request(sp = Depends(get_sp)):
    # TODO: get duration
    stopdur = 30

    # Choose a song that fits the duration criteria
    chosen = None
    durs = list()
    playlists = sp.user_playlists('spotify', limit=50)
    while playlists:
        for pl in playlists['items']:
            tracks = sp.playlist_items(pl['uri'], limit=100)['items']
            for tr in tracks:
                if not tr:
                    continue
                try:
                    trdur = int(tr.get('track', dict()).get('duration_ms', 0)) / 1000.
                except AttributeError:
                    continue
                if abs(trdur - stopdur) < SEC_THRESH:
                    chosen = tr['track']['external_urls']['spotify']
                    break
                else:
                    durs.append(trdur)
            if chosen: break
        if chosen: break
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            break
        # TODO: increment SEC_THRESH if we're having trouble finding a match

    # fallback URL
    if not chosen or bool(os.environ.get("APRIL_FOOLS", "0") == "1"):
        # chosen = "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT?si=c0637df83ee748fe"
        # TODO
        chosen = "no track found"

    return {'url': chosen}

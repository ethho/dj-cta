import os
import requests
from typing import Optional
from fastapi import Depends, FastAPI, APIRouter
from pydantic import BaseModel
from .deps import get_rand_pl

spt_callbacks_router = APIRouter(
    prefix="/spt",
    tags=["spt"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "foobar"}},
)

@spt_callbacks_router.get("/")
def get_random_song(pl = Depends(get_rand_pl)):
    chosen = None
    for tr in sp.playlist_items(pl['uri'], limit=50, offset=randint(0, 20))['items']:
        trdur = int(tr['track']['duration_ms']) / 1000.
        if abs(trdur - stopdur) < SEC_THRESH:
            chosen = tr['track']['external_urls']['spotify']
    if not chosen or bool(os.environ.get("APRIL_FOOLS", "0") == "1"):
        chosen = "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT?si=c0637df83ee748fe"
    return {'url': chosen}

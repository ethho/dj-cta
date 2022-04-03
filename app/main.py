import os
from typing import Optional
from random import randint
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from io import StringIO
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel
from .deps import get_sp

SEC_THRESH = 15
APRIL_FOOLS = False
CTA_ARRIVALS = {
    'base_url': 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?',
    'key': os.environ['CTA_API_KEY']
}
DEBUG = bool(os.environ.get('DEBUG', '0') == '1')
app = FastAPI(debug=DEBUG)

# ---------------------------- Models ------------------------------------------

class LocModel(BaseModel):
    stopid: int
    # description: Optional[str] = None
    # price: float
    # tax: Optional[float] = None

# ----------------------------- Utils ------------------------------------------

async def get_stop_dur(stpid: int, rtid: Optional[str] = None) -> int:
    # Get CTA arrival time from stop ID
    # stpid = 30023
    resp = requests.get(CTA_ARRIVALS['base_url'], params=dict(
        # mapid=None,
        # mapid=40120,
        # stpid=None,
        stpid=stpid,
        # https://www.transitchicago.com/traintracker/arrivaltimes/?sid=40120
        # max=None,
        rt=rtid,
        key=CTA_ARRIVALS['key'],
    ))
    
    # Parse XML response
    tree = ET.parse(StringIO(resp.text))
    root = tree.getroot()
    arrt = root.find('./eta/arrT')
    stcode = root.find('./errCd')
    if int(stcode.text) > 0 or arrt is None:
        detail = f"could not fetch wait time for stop ID '{stpid}'"
        if rtid:
            detail += f" (for route ID '{rtid}')"
        cta_err = root.find('./errNm')
        if cta_err:
            detail += f" (CTA API error: {cta_err.text})"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=detail)

    # Formatted like 20220402 23:20:25
    arr_dt = datetime.strptime(arrt.text, "%Y%m%d %H:%M:%S")
    return int((arr_dt - datetime.now()).seconds)
    # print(f"{stopdur=}")


async def get_track(sp, stopdur: int, tolerance: int):
    # Choose a song that fits the duration criteria
    chosen = None
    durs = list()
    playlists = sp.user_playlists('spotify', limit=50)
    while playlists:
        # TODO: manually add some playlists with really long and really short songs
        for pl in playlists['items']:
            tracks = sp.playlist_items(pl['uri'], limit=100)['items']
            for tr in tracks:
                if not tr:
                    continue
                try:
                    trdur = int(tr.get('track', dict()).get('duration_ms', 0)) / 1000.
                except AttributeError:
                    continue
                secs_diff = trdur - stopdur
                if abs(secs_diff) < tolerance:
                    chosen = {
                        'url': tr['track']['external_urls']['spotify'],
                        'track_duration': int(trdur),
                        'wait_duration': int(stopdur)
                    }
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

    # some logging
    # TODO: https://cloud.google.com/logging/docs/setup/python

    # fallback URL
    if not chosen or APRIL_FOOLS:
        # chosen = "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT?si=c0637df83ee748fe"
        # TODO
        chosen = "no track found"
    return chosen

# ----------------------------- Endpoints --------------------------------------

@app.get("/")
async def song_request(stpid: int, rtid: Optional[str] = None, sp = Depends(get_sp)):
    stopdur = await get_stop_dur(stpid, rtid)
    chosen = await get_track(sp, stopdur, tolerance=SEC_THRESH)
    return chosen

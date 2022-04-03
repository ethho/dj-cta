import os
import time
import asyncio
from math import radians, cos, sin, asin, sqrt
import pandas as pd
from typing import Optional, Union
from random import randint, shuffle
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
from io import StringIO
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Request, Response
from pydantic import BaseModel
from .deps import get_sp

RICK_MODE = False
RICK_OBJ = {
    'url':  "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT?si=c0637df83ee748fe",
    'uri': 'spotify:track:4cOdK2wGLETKBW3PvgPWqT',
    'track_duration': 213,
    'wait_duration': -1,
}
REQUEST_TIMEOUT_ERROR = 30
SEC_THRESH = 15
CTA_ARRIVALS = {
    'base_url': 'http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?',
    'key': os.environ['CTA_API_KEY']
}
ADDITIONAL_PLISTS = [
    {'uri': '5XnkjnyMyg2ZRPBCYVHkbw'},
    {'uri': '71P8SkCDFgziTWkPJDfsRb'},
]
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
    if arrt is None:
        if int(stcode.text) == 0:
            # successful call, just no arrivals anytime soon
            return -1
        detail = f"could not fetch wait time for stop ID '{stpid}'"
        if rtid:
            detail += f" (for route ID '{rtid}')"
        cta_err = root.find('./errNm')
        if cta_err is not None:
            detail += f" (CTA API error: {cta_err.text})"
        # DEBUG
        # detail += f" {resp.text=}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=detail)

    # Formatted like 20220402 23:20:25
    arr_dt = datetime.strptime(arrt.text, "%Y%m%d %H:%M:%S")
    return int((arr_dt - datetime.now()).seconds)
    # print(f"{stopdur=}")


async def get_track(sp, stopdur: int, tolerance: int, start_falloff: int = 1000):
    # -1 means there are no trains arriving soon
    if stopdur < 0:
        return RICK_OBJ
    
    # Choose a song that fits the duration criteria
    init_tol = tolerance
    chosen = None
    durs = list()
    playlists = sp.user_playlists('spotify', limit=50)
    while playlists:
        pls = ADDITIONAL_PLISTS
        # manually add some playlists with really long and really short songs
        pls.extend(playlists['items'])
        # DEBUG 
        # pls = ADDITIONAL_PLISTS
        shuffle(pls)
        for pl in pls:
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
                        'uri': tr['track']['uri'],
                        'track_duration': int(trdur),
                        'wait_duration': int(stopdur)
                    }
                    break
                else:
                    durs.append(trdur)
            if chosen: break
        if chosen: break
        # if (tolerance / init_tol) > 2**6:
        #     raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
        #                          detail=f"couldn't find a track of acceptable length ({stopdur=})")
        elif len(durs) > start_falloff:
            tolerance *= 2.
            print(f"increasing tolerance to {tolerance=}")
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            break
        # TODO: increment SEC_THRESH if we're having trouble finding a match

    # some logging
    # TODO: https://cloud.google.com/logging/docs/setup/python

    # fallback URL
    if not chosen or RICK_MODE:
        chosen = RICK_OBJ
    return chosen


def haversine(row, lon2, lat2):
    return _haversine(row['stop_lon'], row['stop_lat'], lon2, lat2)


def _haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)

    Credit to https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


async def get_nearest_stops(lat: float, lon: float, limit: int = None) -> int:
    '''
    Should use Haversine, but we just do good old Pythagorean
    '''
    if limit is None:
        lim = slice(0, 0)
    else:
        lim = slice(0, limit)
    df = pd.read_csv('app/stops.txt', usecols=[
        'stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'parent_station'
    ])
    df['miles_away'] = df.agg(haversine, axis=1, lon2=lat, lat2=lon)
    df.loc[:, 'parent_station'] = df['parent_station'].fillna(df['stop_id']).astype(int)
    return (
        df
        .drop_duplicates(['parent_station'])
        [df['stop_id'].astype(int) >= 30000]
        .sort_values(by=['miles_away'], ascending=True)
        [['stop_id', 'stop_name', 'miles_away']]
        .to_dict('records')
        [lim]
    )

# ----------------------------- Endpoints --------------------------------------

@app.get("/")
async def song_request(stpid: Union[int, str] = 'nearest', rtid: Optional[str] = None, 
                       sp = Depends(get_sp), lat: Optional[float] = None, lon: Optional[float] = None):
    if stpid == 'nearest':
        if lat is None or lon is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"please pass lat and lon if using nearest station")
        stops = await get_nearest_stops(lat, lon, limit=1)
        if stops:
            stpid = stops[0]['stop_id']
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"could not find a nearest stop for {lat=} {lon=}")
    stopdur = await get_stop_dur(stpid, rtid)
    chosen = await get_track(sp, stopdur, tolerance=SEC_THRESH)
    if chosen['wait_duration'] < 0:
        chosen['detail'] = f"found no arrivals at stop ID {stpid} (route ID {rtid}) in the near future"
    return chosen


@app.get("/nearest_stops")
async def nearest_stops(lat: float, lon: float, limit: Optional[int] = 20):
    limit = min(limit, 20)
    stops = await get_nearest_stops(lat, lon, limit=limit)
    return {'stops': stops}
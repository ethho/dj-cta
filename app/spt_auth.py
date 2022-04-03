import os
import requests
from typing import Optional
import requests
from fastapi import Depends, FastAPI, APIRouter
from pydantic import BaseModel

AUTH_URL = 'https://accounts.spotify.com/api/token'
SPT_SECRET = os.environ['SPT_SECRET']
SPT_CLIENT_ID = os.environ['SPT_CLIENT_ID']
spt_callbacks_router = APIRouter()

@spt_callbacks_router.get('/')
def hello_spt_callbacks():
    """
    TODO
    """

    # url = 'https://accounts.spotify.com/api/token'
    # headers = {'Authorization': f'Basic {SPT_CLIENT_ID}:{SPT_SECRET.encode("utf-8")}'}
    # form = {"grant_type": "client_credentials"}
    # resp = requests.post(url, headers=headers)
    resp = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': SPT_CLIENT_ID,
        'client_secret': SPT_SECRET,
    })
    assert resp.status_code == 200, resp
    return {"msg": f"hello from spt_callbacks_router"}

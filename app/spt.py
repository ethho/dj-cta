import os
import requests
from typing import Optional
from fastapi import Depends, FastAPI, APIRouter
from pydantic import BaseModel
from .deps import get_spt_access_token, get_random_words

spt_callbacks_router = APIRouter()

RANDOMMER_API_KEY=os.environ['RANDOMMER_API_KEY']

@spt_callbacks_router.get("/")
def get_random_song(token = Depends(get_spt_access_token), words = Depends(get_random_words)):
    return {'msg': ", ".join(words)}

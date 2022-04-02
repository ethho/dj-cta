import os
from typing import Optional
from fastapi import Depends, FastAPI
from pydantic import BaseModel


app = FastAPI()

# ---------------------------- Models ------------------------------------------

class SongRequest(BaseModel):
    stopid: int
    # description: Optional[str] = None
    # price: float
    # tax: Optional[float] = None

async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# ---------------------------- Routes ------------------------------------------

@app.get("/hello")
def hello_world():
    name = os.environ.get("NAME", "World")
    return {"Hello": f"{name}"}


@app.get("/")
async def song_request(req: SongRequest, commons: dict = Depends(common_parameters)):
    print(commons)
    return req


import os
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    name = os.environ.get("NAME", "World")
    return {"Hello": f"{name}"}

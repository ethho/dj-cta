import os
from typing import Optional
from random import randint
import requests
from fastapi import Depends, FastAPI, APIRouter
from pydantic import BaseModel
from .deps import get_rand_pl, get_sp

SEC_THRESH = 15
DEBUG = bool(os.environ.get('DEBUG', '0') == '1')
app = FastAPI(debug=DEBUG)

# ---------------------------- Models ------------------------------------------

class LocModel(BaseModel):
    stopid: int
    # description: Optional[str] = None
    # price: float
    # tax: Optional[float] = None


async def cta_creds(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


async def spt_creds(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# ------------------------------- Scratch --------------------------------------

# var authOptions = {
#   url: 'https://accounts.spotify.com/api/token',
#   headers: {
#     'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
#   },
#   form: {
#     grant_type: 'client_credentials'
#   },
#   json: true
# };

# request.post(authOptions, function(error, response, body) {
#   if (!error && response.statusCode === 200) {

#     // use the access token to access the Spotify Web API
#     var token = body.access_token;
#     var options = {
#       url: 'https://api.spotify.com/v1/users/jmperezperez',
#       headers: {
#         'Authorization': 'Bearer ' + token
#       },
#       json: true
#     };
#     request.get(options, function(error, response, body) {
#       console.log(body);
#     });
#   }
# });

# @app.post("/invoices/", callbacks=invoices_callback_router.routes)
# def create_invoice(invoice: Invoice, callback_url: Optional[HttpUrl] = None):
#     """
#     Create an invoice.

#     This will (let's imagine) let the API user (some external developer) create an
#     invoice.

#     And this path operation will:

#     * Send the invoice to the client.
#     * Collect the money from the client.
#     * Send a notification back to the API user (the external developer), as a callback.
#         * At this point is that the API will somehow send a POST request to the
#             external API with the notification of the invoice event
#             (e.g. "payment successful").
#     """
#     # Send the invoice, collect the money, send the notification (the callback)
#     return {"msg": "Invoice received"}



# ---------------------------- Routes ------------------------------------------

# app.include_router(spt_callbacks_router)


@app.get("/hello")
def hello_world(commons: dict = Depends(cta_creds)):
    name = os.environ.get("NAME", "World")
    return {"Hello": f"{name}"}


@app.get("/")
def song_request(sp = Depends(get_sp), playlist_uris = Depends(get_rand_pl)):
    # TODO: get duration
    stopdur = 180

    # Choose a song
    chosen = None
    trs = list()
    for pl in playlist_uris:
        foo = sp.playlist_items(pl['uri'], limit=50, offset=randint(0, 10))['items']
        trs.extend(foo)
    trs = (
        
    )
    chosen = [

    ]

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
    return {'url': chosen}



'''
@spt_callbacks_router.post(
    # "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
    # "{$callback_url}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass
'''



import os
from typing import Optional
import requests
from fastapi import Depends, FastAPI, APIRouter
from pydantic import BaseModel
from .spt import spt_callbacks_router

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

app.include_router(spt_callbacks_router)
app.include_router(
    spt_callbacks_router,
    prefix="/spt",
    tags=["spt"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "foobar"}},
)


@app.get("/hello")
def hello_world(commons: dict = Depends(cta_creds)):
    name = os.environ.get("NAME", "World")
    return {"Hello": f"{name}"}


@app.get("/")
def song_request(stopid: Optional[int] = 0, cta_creds: dict = Depends(cta_creds)):
    # return {"stopid": stopid}
    return {"stopid": DEBUG}



'''
@spt_callbacks_router.post(
    # "{$callback_url}/invoices/{$request.body.id}", response_model=InvoiceEventReceived
    # "{$callback_url}", response_model=InvoiceEventReceived
)
def invoice_notification(body: InvoiceEvent):
    pass
'''



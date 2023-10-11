from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from azure.core.exceptions import ClientAuthenticationError

from betteremail.utils import generate_state, check_id_token_and_return_id_provider, select_oauth_provider, str_to_timestamp
import betteremail.graph as graph

tags_metadata = [
    {
        "name": "public",
        "description": "Endpoints to authenticate users.",
    },
    {
        "name": "private",
        "description": "Manage emails. Endpoints that allow clients to get information and notification about emails.",
    },
]

app = FastAPI(title="Better Email")

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://sheltered-fortress-14848-ca530ca38502.herokuapp.com/"
]

#TODO: CORS allowed for local development. Origins should change
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["public"])
async def probe():
    """
    Liveness probe
    """
    return {"message": "Hello World"}

@app.get('/emails', tags=["private"])
async def emails(since: str, idToken: str):
    """
     This API endpoint returns True if the user has received an email after the timestamps provided in params, False otherwise.
    """
    provider = check_id_token_and_return_id_provider(idToken) #TODO : raise error if idToken not correct
    since = str_to_timestamp(since) #TODO: Handle ERROR    
    
    if provider == "graph":
        try:
            result = graph.has_received_an_email_since(since, idToken)
        except ClientAuthenticationError as e:
            raise HTTPException(status_code=404, detail=e.message)
    else:
        result = "Gmail not available"

    return result

# Route to initiate Microsoft OAuth 2.0 authentication
@app.get("/connect/email", tags=["public"])
def connect(email: str, state: str = Depends(generate_state)):
    """
     This endpoint redirects the client to the matching oauth2 flow.
    """
    # Store the state value in the session for later verification
    url = select_oauth_provider(email, state)
    return RedirectResponse(url)
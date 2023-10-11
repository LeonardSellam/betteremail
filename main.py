from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from azure.core.exceptions import ClientAuthenticationError

from betteremail.utils import generate_state, check_id_token_and_return_id_provider, select_oauth_provider, str_to_timestamp
import betteremail.graph as graph


app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

#TODO: CORS allowed for local development. Origins should change
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/emails')
async def emails(since: str, idToken: str):
    """
     This API endpoint returns a Bool if the user whose idToken matches has received an email since the timestamps provided
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
@app.get("/connect/email")
def connect(email: str, state: str = Depends(generate_state)):
    """
     This API endpoint returns a Bool if the user whose idToken matches has received an email since the timestamps provided
    """
    # Store the state value in the session for later verification
    url = select_oauth_provider(email, state)
    return RedirectResponse(url)
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from azure.core.exceptions import ClientAuthenticationError
import uuid
import requests
import graph

MICROSOFT_AUTH_URL = "https://login.microsoftonline.com/consumers/oauth2/authorize"
GMAIL_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"

CLIENT_ID_MICROSOFT = "be73bf81-df80-40e2-baf7-9f06cec51885"

CLIENT_ID_GMAIL=""
REDIRECT_URI = "http://localhost:8000/callback" 

MICROSOFT_SCOPE = "User.Read Mail.Read email offline_access openid profile"

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to generate a unique state value for CSRF protection
def generate_state():
    return str(uuid.uuid4())

def microsoft_auth_flow_url(state):
    return f"{MICROSOFT_AUTH_URL}?client_id={CLIENT_ID_MICROSOFT}&redirect_uri={REDIRECT_URI}&state={state}&response_type=code&scope={MICROSOFT_SCOPE}&response_mode=query"

def gmail_auth_flow_url(state):
    return f"{GMAIL_AUTH_URL}?client_id={CLIENT_ID_GMAIL}&redirect_uri={REDIRECT_URI}&state={state}&response_type=code&scope=email profile"


def oauth_selection(email, state):
    if "@gmail.com" in email:
        return gmail_auth_flow_url(state)
    if "@microsoft.com" in email:
        return microsoft_auth_flow_url(state)
    else:
        "error"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/emails')
async def emails(since: str, idToken: str):
    since = graph.str_to_timestamp(since) #TODO: Handle ERROR
    try:
        result = graph.has_received_an_email_since(since, idToken)
    except ClientAuthenticationError as e:
        raise HTTPException(status_code=404, detail=e.message)

    return result

# Route to initiate Microsoft OAuth 2.0 authentication
@app.get("/connect/email")
def connect(email: str, state: str = Depends(generate_state)):
    # Store the state value in the session for later verification
    url = oauth_selection(email, state)
    return RedirectResponse(url)


def get_my_emails(obo_token):

    graph_api_endpoint = "https://graph.microsoft.com/v1.0/me"
    
# Set up the request headers with the OBO token
    headers = {
        "Authorization": "Bearer " + str(obo_token),
        "Content-Type": "application/json",
    }
    response = requests.get(graph_api_endpoint, headers=headers)
    if response.status_code == 200:
    # Parse and work with the response data (email messages)
        email_data = response.json()
        for email in email_data.get("value", []):
            print("Email Subject:", email.get("subject"))
        print("Total Email Count:", len(email_data.get("value", [])))
    else:
        print("Error accessing Microsoft Graph API:", response.status_code, response.text)
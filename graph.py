import os
import uuid
from datetime import datetime

from azure.identity import OnBehalfOfCredential
from msgraph.core import GraphClient


MICROSOFT_AUTH_URL = os.getenv("MICROSOFT_AUTH_URL", "https://login.microsoftonline.com/consumers/oauth2/authorize")
GMAIL_AUTH_URL = os.getenv("GMAIL_AUTH_URL", "https://accounts.google.com/o/oauth2/auth")

MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID", "be73bf81-df80-40e2-baf7-9f06cec51885")
MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET", "")

REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/callback")

GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID", "")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET", "")

MICROSOFT_CLIENT_SCOPES = os.getenv("MICROSOFT_CLIENT_SCOPES", "User.Read Mail.Read email offline_access openid profile")
MICROSOFT_API_SCOPES = os.getenv("MICROSOFT_API_SCOPES", "User.Read Mail.Read email")

date_format = '%Y-%m-%dT%H:%M:%S%z'


def get_obo_credentials(idToken):

    credential = OnBehalfOfCredential(
        tenant_id="consumers",
        client_id=MICROSOFT_CLIENT_ID,
        client_secret=MICROSOFT_CLIENT_SECRET,
        user_assertion=idToken,
    )   
    return credential

def user_graph_client(idToken):
    credentials = get_obo_credentials(idToken)
    user_client = GraphClient(credential=credentials, scopes=MICROSOFT_API_SCOPES.split(' '))
    return user_client

def has_received_an_email_since(datetime, idToken):
    endpoint = '/me/mailFolders/inbox/messages'

    select = 'from,isRead,receivedDateTime,subject'

    top = 1
    # Sort by received time, newest first
    order_by = 'receivedDateTime DESC'
    request_url = f'{endpoint}?$select={select}&$top={top}&$orderBy={order_by}'

    response = user_graph_client(idToken).get(request_url)

    if response.status_code == 200:
        last_timestamps = get_last_email_timestamp(response.json())
        return is_older(datetime, last_timestamps)

    response.raise_for_status() 

def get_last_email_timestamp(inbox):
    emails = inbox['value']

    if not emails:
        return False
            
    return str_to_timestamp(list(emails)[0]["receivedDateTime"])

def is_older(tmstp1, tmstp2):
    return tmstp1 < tmstp2 

def str_to_timestamp(st):
    return datetime.strptime(st, date_format)

def generate_state():
    return str(uuid.uuid4())

def microsoft_auth_flow_url(state):
    return f"{MICROSOFT_AUTH_URL}?client_id={MICROSOFT_CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={state}&response_type=code&scope={MICROSOFT_CLIENT_SCOPES}&response_mode=query"

def gmail_auth_flow_url(state):
    return f"{GMAIL_AUTH_URL}?client_id={GMAIL_CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={state}&response_type=code&scope=email profile"


def oauth_selection(email, state):
    if "@gmail.com" in email:
        return gmail_auth_flow_url(state)
    if "@microsoft.com" in email:
        return microsoft_auth_flow_url(state)
    else:
        "error"
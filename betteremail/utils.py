import uuid
from datetime import datetime
import re
from .common import MICROSOFT_AUTH_URL, GMAIL_AUTH_URL, MICROSOFT_CLIENT_ID, REDIRECT_URI, MICROSOFT_CLIENT_SCOPES, GMAIL_CLIENT_ID, DATETIME_FORMAT

EMAIL_REGEX =  r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
GMAIL_SUFFIXES = "@gmail.com"
MICROSOFT_SUFFIXES = "@microsoft.com @outlook.com"

def select_oauth_provider(email, state):
    if(re.fullmatch(EMAIL_REGEX, email)):
        if any(suffix in email for suffix in GMAIL_SUFFIXES.split(" ")):
            return gmail_auth_flow_url(state)
        if any(suffix in email for suffix in MICROSOFT_SUFFIXES.split(" ")):
            return microsoft_auth_flow_url(state)

    return "error"


def microsoft_auth_flow_url(state):
    return f"{MICROSOFT_AUTH_URL}?client_id={MICROSOFT_CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={state}&response_type=code&scope={MICROSOFT_CLIENT_SCOPES}"

def gmail_auth_flow_url(state):
    return f"{GMAIL_AUTH_URL}?client_id={GMAIL_CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={state}&response_type=code&scope=email profile"

def is_older(tmstp1, tmstp2):
    return tmstp1 < tmstp2 

def str_to_timestamp(st):
    return datetime.strptime(st, DATETIME_FORMAT)

def generate_state():
    return str(uuid.uuid4())

def check_id_token_and_return_id_provider(idToken):
    return "graph"
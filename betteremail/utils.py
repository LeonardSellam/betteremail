import uuid
from datetime import datetime
from .common import MICROSOFT_AUTH_URL, GMAIL_AUTH_URL, MICROSOFT_CLIENT_ID, REDIRECT_URI, MICROSOFT_CLIENT_SCOPES, GMAIL_CLIENT_ID, DATETIME_FORMAT


def select_oauth_provider(email, state):
    if "@gmail.com" in email:
        return gmail_auth_flow_url(state)
    if "@microsoft.com" in email:
        return microsoft_auth_flow_url(state)
    else:
        return "error"


def microsoft_auth_flow_url(state):
    return f"{MICROSOFT_AUTH_URL}?client_id={MICROSOFT_CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={state}&response_type=code&scope={MICROSOFT_CLIENT_SCOPES}&response_mode=query"

def gmail_auth_flow_url(state):
    return f"{GMAIL_AUTH_URL}?client_id={GMAIL_CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={state}&response_type=code&scope=email profile"

def is_older(tmstp1, tmstp2):
    return tmstp1 < tmstp2 

def str_to_timestamp(st):
    return datetime.strptime(st, DATETIME_FORMAT)

def generate_state():
    return str(uuid.uuid4())
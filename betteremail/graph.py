
from azure.identity import OnBehalfOfCredential
from msgraph.core import GraphClient
from .utils import is_older, str_to_timestamp
from .common import MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET, MICROSOFT_API_SCOPES


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
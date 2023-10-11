import os

MICROSOFT_AUTH_URL = os.getenv("MICROSOFT_AUTH_URL", "https://login.live.com/oauth20_authorize.srf")
GMAIL_AUTH_URL = os.getenv("GMAIL_AUTH_URL", "https://accounts.google.com/o/oauth2/auth")

MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID", "be73bf81-df80-40e2-baf7-9f06cec51885")
MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET", "")

REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/callback")

GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID", "")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET", "")

MICROSOFT_CLIENT_SCOPES = os.getenv("MICROSOFT_CLIENT_SCOPES", "https://graph.microsoft.com/.default")
MICROSOFT_API_SCOPES = os.getenv("MICROSOFT_API_SCOPES", "User.Read Mail.Read email")

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
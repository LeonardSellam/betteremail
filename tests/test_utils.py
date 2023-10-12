from betteremail.utils import select_oauth_provider, is_older, generate_state, str_to_timestamp
from datetime import datetime, timezone

def test_select_oauth_provider_when_microsoft():
    result_microsoft = select_oauth_provider("leo@microsoft.com", "123")
    assert result_microsoft == "https://login.live.com/oauth20_authorize.srf?client_id=be73bf81-df80-40e2-baf7-9f06cec51885&redirect_uri=http://localhost:8000/callback&state=123&response_type=code&scope=https://graph.microsoft.com/.default"

    result_outlook = select_oauth_provider("leo@outlook.com", "789")
    assert result_outlook == "https://login.live.com/oauth20_authorize.srf?client_id=be73bf81-df80-40e2-baf7-9f06cec51885&redirect_uri=http://localhost:8000/callback&state=789&response_type=code&scope=https://graph.microsoft.com/.default"

def test_select_oauth_provider_when_gmail():
    result = select_oauth_provider("leo@gmail.com", "123")
    print(result)
    assert result == "https://accounts.google.com/o/oauth2/auth?client_id=&redirect_uri=http://localhost:8000/callback&state=123&response_type=code&scope=email profile"

def test_select_oauth_provider_when_other_provider():
    result = select_oauth_provider("leo@tesla.com", "123")
    assert result == "error"

def test_is_older():
    tm1 = datetime(2023, 10, 17)
    tm2 = datetime(2020, 5, 17)
    tm3 = datetime(2024, 5, 2)

    assert is_older(tm2, tm1)
    assert is_older(tm1, tm3)

def test_generate_state():
    assert len(generate_state()) == 36

def test_str_to_timestamp():
    st = "2022-10-11T13:20:59Z"
    assert str_to_timestamp(st) == datetime(2022, 10, 11, 13, 20, 59, tzinfo=timezone.utc)
    



from betteremail.graph import get_last_email_timestamp, has_received_an_email_since

import requests
from unittest.mock import Mock
from unittest import mock, TestCase
from datetime import datetime, timezone

def test_get_last_email_timestamp_when_no_emails():
    inbox = {}
    assert get_last_email_timestamp(inbox) < datetime(1900, 1, 1)

def test_get_last_email_timestamp_when_one_email():
    inbox = {'value': [{'receivedDateTime': '2022-10-11T13:20:59Z'}]}
    result = get_last_email_timestamp(inbox)

    assert result == datetime(2022, 10, 11, 13, 20, 59, tzinfo=timezone.utc)

def test_get_last_email_timestamp_when_mulitple_email():
    inbox = {'value': [{'receivedDateTime': '2022-10-11T13:20:59Z'}, {'receivedDateTime': '2021-10-11T13:20:59Z'}]}
    result = get_last_email_timestamp(inbox)

    assert result == datetime(2022, 10, 11, 13, 20, 59, tzinfo=timezone.utc)


@mock.patch('betteremail.graph.user_graph_client')
def test_has_received_an_email_since(client_mocker):
    mock = Mock()

    mock_2 = Mock(status_code=200)
    mock_2.json.side_effect = [ {'value': [{'receivedDateTime': '2022-10-11T13:20:59Z'}]}, {'value': [{'receivedDateTime': '2022-10-11T13:20:59Z'}]}  ]

    mock.get.side_effect = [mock_2, mock_2]

    client_mocker.side_effect = [mock, mock]

    assert has_received_an_email_since(datetime(2022, 9, 11, 13, 20, 59, tzinfo=timezone.utc), "mytoken")
    assert not has_received_an_email_since(datetime(2022, 11, 11, 13, 20, 59, tzinfo=timezone.utc), "mytoken")

    mock.get.assert_called_with("/me/mailFolders/inbox/messages?$select=from,isRead,receivedDateTime,subject&$top=1&$orderBy=receivedDateTime DESC")
    client_mocker.assert_called_with("mytoken")
import pytest
from unittest.mock import MagicMock, patch
from main import get_tenor_url

@patch('requests.get')
def test_get_tenor_url_ok(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'results': [{'url': 'https://tenor.com/view/cat-gif'}]
    }
    mock_get.return_value = mock_response

    url = get_tenor_url(["test_term"])
    assert url == 'https://tenor.com/view/cat-gif'

@patch('requests.get')
def test_get_tenor_url_empty(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    url = get_tenor_url(["test"])
    assert url is None
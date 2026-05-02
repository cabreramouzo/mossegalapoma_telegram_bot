import pytest
from unittest.mock import MagicMock, patch
from main import get_giphy_url

from unittest.mock import MagicMock, patch
from utils import get_giphy_url

@patch('utils.GIPHY_API_KEY', 'fake_test_key')
@patch('requests.get')
def test_get_giphy_url_ok(mock_get):
    # 1. Configure Mock of Giphy response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': [
            {
                'images': {
                    'original': {
                        'url': 'https://media.giphy.com/media/cat.gif'
                    }
                }
            }
        ]
    }
    mock_get.return_value = mock_response

    # 2. Execute the function
    url = get_giphy_url(["test_term"])

    # 3. Verificamos que extrae la URL correcta de la estructura 'data'
    assert url == 'https://media.giphy.com/media/cat.gif'

    # Opcional: Verificar que se llamó a la URL de Giphy
    args, _ = mock_get.call_args
    assert "api.giphy.com" in args[0]

@patch('requests.get')
def test_get_giphy_url_empty(mock_get):
    """Prueba el caso donde la API responde con error o sin datos."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    url = get_giphy_url(["test"])
    
    assert url is None
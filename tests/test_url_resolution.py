import pytest
from unittest.mock import MagicMock, patch
from amazon import get_real_url_from_shortlink

@patch('requests.get')
def test_get_real_url_success(mock_get):
    # Simulamos que requests.get devuelve un objeto con la propiedad .url
    mock_response = MagicMock()
    mock_response.url = "https://www.amazon.es/producto-largo-original"
    mock_get.return_value = mock_response

    url_final = get_real_url_from_shortlink("https://amzn.eu/short")
    
    assert url_final == "https://www.amazon.es/producto-largo-original"
    mock_get.assert_called_once()

@patch('requests.get')
def test_get_real_url_failure(mock_get):
    # Si la red falla, la función debería devolver la URL original por seguridad
    mock_get.side_effect = Exception("Timeout")
    url_final = get_real_url_from_shortlink("https://amzn.eu/short")
    assert url_final == "https://amzn.eu/short"
import pytest
from unittest.mock import MagicMock
# Importamos las listas y la lógica del archivo principal (asumiendo que se llama main.py)
from main import HASHTAGS_PROPOSTA, FEDERRATES, PALASACA 

def test_hashtag_lists_integrity():
    """Verifica que no se hayan borrado etiquetas críticas por error"""
    assert '#proposta' in HASHTAGS_PROPOSTA
    assert '#federrates' in FEDERRATES
    assert '#palasaca' in PALASACA

@pytest.mark.parametrize("mensaje, esperado", [
    ("Esto es una #proposta importante", True),
    ("No hay etiquetas aquí", False),
    ("Mando una #federrates técnica", True),
    ("He comprado algo #palasaca!", True),
])
def test_detection_logic(mensaje, esperado):
    """Test de lógica pura: ¿detectamos lo que debemos?"""
    texto_low = mensaje.lower()
    detectado = any(h in texto_low for h in HASHTAGS_PROPOSTA + FEDERRATES + PALASACA)
    assert detectado == esperado
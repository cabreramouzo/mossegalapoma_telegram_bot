import pytest
from unittest.mock import MagicMock, AsyncMock
from main import main_handler

@pytest.mark.asyncio
async def test_hora_command():
    mock_update = MagicMock()
    mock_context = MagicMock()
    mock_msg = AsyncMock()
    mock_update.effective_message = mock_msg
    
    # Simulamos que el usuario escribe /hora
    mock_msg.text = "/hora"
    # Añadimos la entidad de comando para que el bot la reconozca (opcional según tu lógica)
    
    # En tu código original, 'hora' era una función aparte, 
    # pero si la integraste en el main_handler, testeamos así:
    from main import hora
    await hora(mock_update, mock_context)
    
    assert mock_msg.reply_text.called
    # Obtenemos los argumentos de la última llamada
    args, kwargs = mock_msg.reply_text.call_args
    
    # Verificamos si el texto está en el primer argumento posicional 
    # o en el argumento con nombre 'text'
    texto_enviado = args[0] if args else kwargs.get('text', "")
    
    assert "202" in texto_enviado
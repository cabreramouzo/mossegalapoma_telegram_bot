import pytest
from unittest.mock import MagicMock, AsyncMock
from main import main_handler

@pytest.mark.asyncio
async def test_troll_detection_short_message():
    mock_update = MagicMock()
    mock_context = MagicMock()
    mock_msg = AsyncMock()
    mock_update.effective_message = mock_msg
    
    # Mensaje de menos de 20 caracteres
    mock_msg.text = "Esto es #proposta" 
    mock_msg.from_user.username = "troll_man"
    mock_msg.reply_to_message = None
    mock_update.edited_message = None
    
    await main_handler(mock_update, mock_context)
    
    # Verificamos que NO se envió al grupo de propuestas
    assert not mock_context.bot.send_message.called
    # Verificamos que el bot respondió al usuario (probablemente con un mensaje de troll)
    assert mock_msg.reply_text.called

@pytest.mark.asyncio
async def test_ignore_non_text_updates():
    mock_update = MagicMock()
    # Simulamos un mensaje que es solo una notificación de sistema (sin texto ni caption)
    mock_update.effective_message.text = None
    mock_update.effective_message.caption = None
    mock_context = MagicMock()
    
    # No debería lanzar ninguna excepción
    await main_handler(mock_update, mock_context)
    
    # No debería haber respondido nada
    assert not mock_update.effective_message.reply_text.called
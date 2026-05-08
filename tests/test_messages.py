import pytest
import random
from unittest.mock import MagicMock, AsyncMock, patch
from main import main_handler

@pytest.mark.asyncio
async def test_main_handler_forward_format():
    mock_update = MagicMock()
    mock_context = MagicMock()
    
    # Creamos un mock específico para el mensaje y lo asíncronizamos
    mock_msg = AsyncMock()
    mock_update.effective_message = mock_msg
    mock_context.bot.send_message = AsyncMock()
    
    # Datos de entrada
    mock_msg.text = "Propuesta con #proposta"
    mock_msg.from_user.username = "joan_demo"
    mock_msg.from_user.first_name = "Joan"
    mock_msg.from_user.last_name = "García"
    mock_msg.reply_to_message = None
    
    await main_handler(mock_update, mock_context)

    # Verificamos que se llamó al envío al grupo
    assert mock_context.bot.send_message.called
    args, kwargs = mock_context.bot.send_message.call_args
    assert "joan_demo (Joan García): Propuesta con #proposta" in kwargs['text']

@pytest.mark.asyncio
async def test_photo_caption_with_hashtag():
    with patch('handlers.random.random', return_value=0.1), \
         patch('amazon.add_afiliats_tag', new_callable=AsyncMock, return_value=[]):
        
        import main
        main.PALASACA = ["#palasaca"]
        
        mock_update = MagicMock()
        mock_context = MagicMock()
        
        class MockMessage:
            def __init__(self):
                # CAMBIO CLAVE: Ponemos un string vacío en lugar de None
                # para que el 'if not (msg.text or msg.caption)' no nos eche
                self.text = "" 
                self.caption = "#palasaca"
                self.from_user = MagicMock(username="test", first_name="T", last_name="U")
                self.reply_text = AsyncMock()
                self.reply_animation = AsyncMock()
            
            def parse_entities(self, types=None): return {}

        msg_obj = MockMessage()
        mock_update.effective_message = msg_obj

        await main.main_handler(mock_update, mock_context)

        assert msg_obj.reply_text.called or msg_obj.reply_animation.called
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from main import main_handler

@pytest.mark.asyncio
async def test_amazon_shortlink_conversion():
    with patch('amazon.get_real_url_from_shortlink') as mock_resolve:
        mock_resolve.return_value = "https://www.amazon.es/dp/B0123456"
        
        mock_update = MagicMock()
        mock_context = MagicMock()
        
        # 1. El mensaje es asíncrono (para reply_text), 
        # pero parse_entities DEBE ser síncrono
        mock_msg = AsyncMock()
        mock_msg.parse_entities = MagicMock()
        
        mock_update.effective_message = mock_msg
        mock_msg.text = "Mira esto: https://amzn.eu/d/5L8fG1"
        
        from telegram import MessageEntity
        entity = MessageEntity(type="url", offset=11, length=22)
        
        # 2. Ahora esto devolverá un dict normal, no una corrutina
        mock_msg.parse_entities.return_value = {entity: "https://amzn.eu/d/5L8fG1"}
        
        from main import main_handler
        await main_handler(mock_update, mock_context)
        
        # 3. Verificamos la respuesta
        expected_link = "https://www.amazon.es/dp/B0123456&tag=pempins-21"
        
        # Comprobamos que reply_text fue llamado con el link correcto
        called_texts = [call.args[0] for call in mock_msg.reply_text.call_args_list]
        assert any(expected_link in t for t in called_texts)
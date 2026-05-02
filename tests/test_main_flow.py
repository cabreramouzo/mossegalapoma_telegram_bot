import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from amazon import get_real_url_from_shortlink, add_afiliats_tag

@pytest.mark.asyncio
async def test_main_calls_amazon_handler(mock_msg_factory):
    # 1. Creamos un mensaje con link de Amazon
    msg = mock_msg_factory(text="Mira este producto: https://amazon.es/dp/1234")
    update = MagicMock(effective_message=msg)
    
    # 2. Parcheamos la función de amazon.py
    with patch('main.handle_amazon_links', new_callable=AsyncMock) as mock_amazon_handler:
        from main import main_handler
        await main_handler(update, MagicMock())
        
        # 3. Verificamos que el main DELEGÓ la tarea al handler de Amazon
        assert mock_amazon_handler.called
        assert mock_amazon_handler.call_args.args[0] == msg
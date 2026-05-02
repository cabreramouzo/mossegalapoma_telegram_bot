import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from main import handle_direct_proposal, handle_reply_proposal

@pytest.mark.asyncio
async def test_direct_only_text(mock_msg_factory):
    """Caso: Mensaje con solo texto y #proposta"""
    mock_context = MagicMock()
    mock_context.bot.send_message = AsyncMock()
    
    msg = mock_msg_factory(text="Esta es una propuesta directa #proposta muy larga")
    update = MagicMock(effective_message=msg)
    
    await handle_direct_proposal(update, mock_context, is_proposal=True)
    
    assert mock_context.bot.send_message.called
    args, kwargs = mock_context.bot.send_message.call_args
    assert "Esta es una propuesta directa" in kwargs['text']

@pytest.mark.asyncio
async def test_direct_photo_with_caption(mock_msg_factory):
    """Caso: Foto con #proposta en el pie de foto (no debe perderse el caption)"""
    mock_context = MagicMock()
    mock_context.bot.copy_message = AsyncMock()
    
    # Importante: text=None, el hashtag está en el caption
    msg = mock_msg_factory(caption="Mirad esta foto #proposta para el podcast")
    msg.photo = [MagicMock()]
    update = MagicMock(effective_message=msg)
    
    await handle_direct_proposal(update, mock_context, is_proposal=True)
    
    assert mock_context.bot.copy_message.called
    args, kwargs = mock_context.bot.copy_message.call_args
    # Verificamos que el caption final contiene el header + el texto original
    assert "Proposta de" in kwargs['caption']
    assert "#proposta para el podcast" in kwargs['caption']

# Reply proposals tests:

@pytest.mark.asyncio
async def test_reply_original_is_text(mock_msg_factory):
    """Caso: Mensaje A (Texto) <- Mensaje B (#proposta)"""
    mock_context = MagicMock()
    mock_context.bot.copy_message = AsyncMock(return_value=MagicMock(message_id=100))
    mock_context.bot.send_message = AsyncMock()
    
    msg_b = mock_msg_factory(text="#proposta comentario")
    msg_a = mock_msg_factory(text="Esta es la idea original")
    msg_b.reply_to_message = msg_a
    
    update = MagicMock(effective_message=msg_b)
    
    await handle_reply_proposal(update, mock_context, is_proposal=True)
    
    # Verificamos que copia el mensaje A
    assert mock_context.bot.copy_message.called
    # Verificamos que el comentario del mensaje B va en el segundo mensaje
    args, kwargs = mock_context.bot.send_message.call_args
    assert "comentario" in kwargs['text']
    assert "Esta es la idea original" not in kwargs['text'] # Porque va en el copy_message

@pytest.mark.asyncio
async def test_reply_original_is_image(mock_msg_factory):
    """Caso: Mensaje A (Foto) <- Mensaje B (#proposta)"""
    mock_context = MagicMock()
    # copy_message DEBE ser AsyncMock porque usas await
    mock_context.bot.copy_message = AsyncMock(return_value=MagicMock(message_id=101))
    # send_message DEBE ser AsyncMock porque usas await
    mock_context.bot.send_message = AsyncMock()
    
    msg_b = mock_msg_factory(text="#proposta")
    # ASEGURAMOS que reply_text sea awaitable
    msg_b.reply_text = AsyncMock() 
    
    msg_a = mock_msg_factory(caption="Foto de un prototipo")
    msg_a.photo = [MagicMock()] 
    
    # IMPORTANTE: Vinculamos el reply
    msg_b.reply_to_message = msg_a
    
    update = MagicMock(effective_message=msg_b)
    
    # Ahora ya no debería fallar el await
    await handle_reply_proposal(update, mock_context, is_proposal=True)
    
    # Verificación
    assert mock_context.bot.copy_message.called
    assert mock_context.bot.copy_message.call_args.kwargs['message_id'] == 999
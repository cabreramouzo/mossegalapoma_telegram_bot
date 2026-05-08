import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from telegram import MessageEntity
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
    """Caso: Mensaje A (Texto) <- Mensaje B (#proposta) → forward + info message"""
    mock_context = MagicMock()
    mock_context.bot.forward_message = AsyncMock(return_value=MagicMock(message_id=100))
    mock_context.bot.send_message = AsyncMock()

    msg_b = mock_msg_factory(text="#proposta comentari")
    msg_a = mock_msg_factory(text="Esta es la idea original")
    msg_b.reply_to_message = msg_a

    update = MagicMock(effective_message=msg_b)

    await handle_reply_proposal(update, mock_context, is_proposal=True)

    assert mock_context.bot.forward_message.called
    assert mock_context.bot.send_message.called
    info_text = mock_context.bot.send_message.call_args.kwargs['text']
    assert "Proposta de" in info_text
    assert "Caçada per" in info_text
    assert "comentari" in info_text

@pytest.mark.asyncio
async def test_reply_original_is_image(mock_msg_factory):
    """Caso: forward falla → fallback a send_message con nota de adjunto + info message"""
    mock_context = MagicMock()
    mock_context.bot.forward_message = AsyncMock(side_effect=Exception("The message can't be forwarded"))
    mock_context.bot.send_message = AsyncMock(return_value=MagicMock(message_id=101))

    msg_b = mock_msg_factory(text="#proposta")
    msg_b.reply_text = AsyncMock()

    msg_a = mock_msg_factory(caption="Foto de un prototipo")
    msg_a.photo = [MagicMock()]

    msg_b.reply_to_message = msg_a

    update = MagicMock(effective_message=msg_b)

    await handle_reply_proposal(update, mock_context, is_proposal=True)

    assert mock_context.bot.send_message.called
    first_call_text = mock_context.bot.send_message.call_args_list[0].kwargs['text']
    assert "adjunt" in first_call_text or "Foto de un prototipo" in first_call_text


@pytest.mark.asyncio
async def test_direct_proposal_preserves_formatting(mock_msg_factory):
    """
    Bold/strikethrough/italic entities from the original message must be
    forwarded to the proposals group with their offsets shifted to account
    for the prepended header string.
    """
    from handlers import handle_direct_proposal, shift_entities

    mock_context = MagicMock()
    mock_context.bot.send_message = AsyncMock()

    msg = mock_msg_factory(text="Proposta amb text en negreta #proposta i contingut")
    # Simulate a bold entity starting at offset 14 ("text en negreta")
    bold_entity = MessageEntity(type=MessageEntity.BOLD, offset=14, length=15)
    msg.entities = [bold_entity]

    update = MagicMock(effective_message=msg, edited_message=None)

    await handle_direct_proposal(update, mock_context, is_proposal=True)

    assert mock_context.bot.send_message.called
    call_kwargs = mock_context.bot.send_message.call_args.kwargs

    # Must use entities, not parse_mode, to preserve formatting
    assert call_kwargs.get('parse_mode') is None
    assert 'entities' in call_kwargs
    sent_entities = call_kwargs['entities']
    assert len(sent_entities) == 1
    assert sent_entities[0].type == MessageEntity.BOLD

    # Offset must be shifted by the UTF-16 length of the header
    header = "💡 Proposta de user_test (TestName TestLast): "
    expected_shift = len(header.encode('utf-16-le')) // 2
    assert sent_entities[0].offset == bold_entity.offset + expected_shift
    assert sent_entities[0].length == bold_entity.length
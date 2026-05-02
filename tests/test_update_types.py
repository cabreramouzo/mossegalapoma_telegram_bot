import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from main import main_handler


@pytest.mark.asyncio
async def test_reaction_does_not_trigger_bot():
    """
    Adding a reaction to a message must NOT trigger any bot response.

    Reactions arrive as a 'message_reaction' update type in Telegram's Bot API.
    PTB sets update.effective_message to None for these updates, and the
    filters.TEXT | filters.CAPTION handler filter won't match them either.
    This test guards the early-return path inside main_handler.
    """
    mock_update = MagicMock()
    mock_context = MagicMock()

    # Simulate a reaction update: no message or caption, just a reaction event
    mock_update.effective_message = None

    await main_handler(mock_update, mock_context)

    # The bot must not have sent or forwarded anything
    mock_context.bot.send_message.assert_not_called()
    mock_context.bot.forward_message.assert_not_called()
    mock_context.bot.copy_message.assert_not_called()


@pytest.mark.asyncio
async def test_edited_message_calls_handle_edited_proposal():
    """
    Editing a message with a proposal hashtag must call handle_edited_proposal,
    NOT handle_direct_proposal or handle_reply_proposal.
    """
    mock_update = MagicMock()
    mock_context = MagicMock()

    mock_msg = AsyncMock()
    mock_msg.text = "Proposta editada amb contingut #proposta suficientment llarg"
    mock_msg.caption = None
    mock_msg.from_user.username = "editor_user"
    mock_msg.from_user.first_name = "Editor"
    mock_msg.from_user.last_name = "User"
    mock_msg.reply_to_message = None

    mock_update.effective_message = mock_msg
    # Mark the update as an edited_message (not a new message)
    mock_update.edited_message = mock_msg

    with patch('main.handle_edited_proposal', new_callable=AsyncMock) as mock_edited, \
         patch('main.handle_direct_proposal', new_callable=AsyncMock) as mock_direct:

        await main_handler(mock_update, mock_context)

        assert mock_edited.called, "handle_edited_proposal should be called for edited messages"
        assert not mock_direct.called, "handle_direct_proposal must NOT be called for edited messages"


@pytest.mark.asyncio
async def test_edited_proposal_sends_edit_confirmation(mock_msg_factory):
    """
    handle_edited_proposal must reply with a TEXT_REPLY_EDITED_PROPOSAL message
    and forward the edited content to the proposals group.
    """
    from handlers import handle_edited_proposal
    from constants import TEXT_REPLY_EDITED_PROPOSAL

    mock_context = MagicMock()
    mock_context.bot.send_message = AsyncMock()

    msg = mock_msg_factory(text="Proposta editada amb hashtag #proposta i contingut")
    update = MagicMock(effective_message=msg, edited_message=msg)

    await handle_edited_proposal(update, mock_context, is_proposal=True)

    # Must reply to the user with an edit-specific confirmation
    assert msg.reply_text.called
    sent_reply = msg.reply_text.call_args.args[0]
    assert sent_reply in TEXT_REPLY_EDITED_PROPOSAL

    # Must forward the edited proposal to the proposals group
    assert mock_context.bot.send_message.called
    sent_text = mock_context.bot.send_message.call_args.kwargs['text']
    assert "editada" in sent_text


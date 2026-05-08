import pytest
from unittest.mock import MagicMock, AsyncMock, patch


@pytest.fixture(autouse=True)
def mock_firestore_db():
    """Patch the Firestore client so tests never hit a real database."""
    with patch('message_store.db') as mock_db:
        yield mock_db


@pytest.fixture
def mock_msg_factory():
    def _create(text=None, caption=None, username="user_test"):
        msg = MagicMock()
        msg.text = text
        msg.caption = caption
        msg.chat_id = 12345
        msg.message_id = 999
        msg.from_user.username = username
        msg.from_user.first_name = "TestName"
        msg.from_user.last_name = "TestLast"
        msg.reply_to_message = None
        # Importante: Que los métodos de respuesta sean AsyncMocks
        msg.reply_text = AsyncMock()
        msg.reply_animation = AsyncMock()
        return msg
    return _create
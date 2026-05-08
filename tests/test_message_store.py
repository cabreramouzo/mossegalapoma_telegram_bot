import pytest
from unittest.mock import MagicMock, patch
from message_store import get_text_hash, save_message_hash, load_message_hash, text_has_changed


def make_msg(chat_id=111, message_id=42):
    msg = MagicMock()
    msg.chat_id = chat_id
    msg.message_id = message_id
    return msg


# ---------------------------------------------------------------------------
# get_text_hash
# ---------------------------------------------------------------------------

def test_get_text_hash_is_deterministic():
    assert get_text_hash("hello") == get_text_hash("hello")


def test_get_text_hash_differs_for_different_texts():
    assert get_text_hash("hello") != get_text_hash("world")


def test_get_text_hash_is_sha256():
    import hashlib
    text = "Proposta de film: #proposta"
    expected = hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert get_text_hash(text) == expected


# ---------------------------------------------------------------------------
# save_message_hash
# ---------------------------------------------------------------------------

def test_save_message_hash_writes_correct_hash(mock_firestore_db):
    msg = make_msg()
    text = "Proposta nova #proposta"

    save_message_hash(msg, text)

    # Firestore .set() must have been called once
    doc_ref = mock_firestore_db.collection.return_value.document.return_value
    doc_ref.set.assert_called_once()

    saved_doc = doc_ref.set.call_args.args[0]
    assert saved_doc["hash"] == get_text_hash(text)
    assert saved_doc["chat_id"] == msg.chat_id
    assert saved_doc["message_id"] == msg.message_id
    assert "updated_at" in saved_doc
    assert "expires_at" in saved_doc


def test_save_message_hash_ttl_is_set(mock_firestore_db):
    from datetime import timedelta
    msg = make_msg()

    save_message_hash(msg, "some text")

    saved_doc = mock_firestore_db.collection.return_value.document.return_value.set.call_args.args[0]
    delta = saved_doc["expires_at"] - saved_doc["updated_at"]
    assert delta == timedelta(hours=72)


# ---------------------------------------------------------------------------
# load_message_hash
# ---------------------------------------------------------------------------

def test_load_message_hash_returns_hash_when_exists(mock_firestore_db):
    msg = make_msg()
    expected_hash = get_text_hash("original text")

    snap = mock_firestore_db.collection.return_value.document.return_value.get.return_value
    snap.exists = True
    snap.to_dict.return_value = {"hash": expected_hash}

    result = load_message_hash(msg)

    assert result == expected_hash


def test_load_message_hash_returns_none_when_not_exists(mock_firestore_db):
    msg = make_msg()

    snap = mock_firestore_db.collection.return_value.document.return_value.get.return_value
    snap.exists = False

    result = load_message_hash(msg)

    assert result is None


# ---------------------------------------------------------------------------
# text_has_changed — the core feature:
# detect real user edits vs. Telegram auto-updates (e.g. YouTube previews)
# ---------------------------------------------------------------------------

def test_text_has_changed_returns_true_when_no_previous_hash(mock_firestore_db):
    """No stored hash → treat as changed to avoid missing a real edit."""
    msg = make_msg()

    snap = mock_firestore_db.collection.return_value.document.return_value.get.return_value
    snap.exists = False

    assert text_has_changed(msg, "any text") is True


def test_text_has_changed_returns_false_when_text_is_same(mock_firestore_db):
    """Same text (e.g. Telegram updated the YouTube preview) → NOT changed."""
    msg = make_msg()
    text = "Mira aquest video de youtube #proposta https://youtu.be/abc123"

    snap = mock_firestore_db.collection.return_value.document.return_value.get.return_value
    snap.exists = True
    snap.to_dict.return_value = {"hash": get_text_hash(text)}

    assert text_has_changed(msg, text) is False


def test_text_has_changed_returns_true_when_text_differs(mock_firestore_db):
    """User genuinely edited the text → changed."""
    msg = make_msg()
    original = "Proposta original #proposta"
    edited = "Proposta editada amb més detalls #proposta"

    snap = mock_firestore_db.collection.return_value.document.return_value.get.return_value
    snap.exists = True
    snap.to_dict.return_value = {"hash": get_text_hash(original)}

    assert text_has_changed(msg, edited) is True


def test_text_has_changed_uses_correct_document_key(mock_firestore_db):
    """The Firestore document is keyed by 'chat_id:message_id'."""
    msg = make_msg(chat_id=999, message_id=7)

    snap = mock_firestore_db.collection.return_value.document.return_value.get.return_value
    snap.exists = False

    text_has_changed(msg, "text")

    mock_firestore_db.collection.return_value.document.assert_called_with("999:7")

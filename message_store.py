import hashlib
from datetime import datetime, timedelta, timezone
from google.cloud import firestore

db = firestore.Client()
MESSAGE_HASH_COLLECTION = "telegram_message_hashes"
MESSAGE_HASH_TTL_HOURS = 72


def get_message_key(msg):
    return f"{msg.chat_id}:{msg.message_id}"


def get_text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_message_hash_ref(msg):
    return db.collection(MESSAGE_HASH_COLLECTION).document(get_message_key(msg))


def save_message_hash(msg, text: str):
    now = datetime.now(timezone.utc)

    get_message_hash_ref(msg).set({
        "hash": get_text_hash(text),
        "chat_id": msg.chat_id,
        "message_id": msg.message_id,
        "updated_at": now,
        "expires_at": now + timedelta(hours=MESSAGE_HASH_TTL_HOURS),
    })


def load_message_hash(msg):
    snap = get_message_hash_ref(msg).get()

    if not snap.exists:
        return None

    return snap.to_dict().get("hash")


def text_has_changed(msg, text: str) -> bool:
    previous_hash = load_message_hash(msg)

    if previous_hash is None:
        # Don't know the previous hash,
        # assume it has changed to avoid missing a real edit.
        return True

    return previous_hash != get_text_hash(text)

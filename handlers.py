from telegram import Update, MessageEntity, constants
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import random
from constants import GROUP_PROPOSALS, TEXT_REPLY_ERRATA, TEXT_REPLY_PROPOSAL, TEXT_REPLY_EDITED_PROPOSAL, TEXT_REPLY_PALASACA, TEXT_REPLY_NETFLIX
from utils import get_giphy_url


def shift_entities(entities, header):
    """
    Returns new entities with offsets shifted to account for a prepended header.
    Telegram entity offsets are counted in UTF-16 code units, so emoji and
    other non-BMP characters count as 2 units each.
    """
    if not entities:
        return None
    offset_shift = len(header.encode('utf-16-le')) // 2
    return [
        MessageEntity(
            type=e.type,
            offset=e.offset + offset_shift,
            length=e.length,
            url=e.url,
            user=e.user,
            language=e.language,
            custom_emoji_id=e.custom_emoji_id,
        )
        for e in entities
    ]

async def handle_reply_proposal(update, context, is_proposal):
    msg = update.effective_message
    target_msg = msg.reply_to_message
    content_text = (target_msg.text or target_msg.caption or "")
    print(f"Group id {msg.chat_id} - User {target_msg.from_user.id} - Content: {content_text[:30]}...")
    # Confirmation in the group
    await msg.reply_text(random.choice(TEXT_REPLY_PROPOSAL) if is_proposal else random.choice(TEXT_REPLY_ERRATA))

    # STEP 1: Forward the original message (shows "Forwarded from..." header with author and chat)
    sent_msg = await context.bot.forward_message(
        chat_id=GROUP_PROPOSALS,
        from_chat_id=target_msg.chat_id,
        message_id=target_msg.message_id
    )

    # STEP 2: Submission info + moderator comment
    orig_user = target_msg.from_user
    orig_display = f"{orig_user.username} ({orig_user.first_name})"
    
    info_text = (
        f"💡 **Proposta de:** {orig_display}\n"
        f"👤 **Caçada per:** @{msg.from_user.username}\n"
        f"💬 **Comentari original:** {msg.text or msg.caption}"
    )

    await context.bot.send_message(
        chat_id=GROUP_PROPOSALS,
        text=info_text,
        reply_to_message_id=sent_msg.message_id,
        parse_mode="Markdown"
    )


async def handle_direct_proposal(update, context, is_proposal):
    msg = update.effective_message
    user_text = (msg.text or msg.caption or "")
    
    if is_proposal and len(user_text) < 20:
        await msg.reply_text(f"Això no té pinta de proposta... 😒")
        return

    # Confirmation
    await msg.reply_text(random.choice(TEXT_REPLY_PROPOSAL) if is_proposal else "Anoto la fe d'errates! 📝")

    # Header to identify the author
    user = msg.from_user
    user_display = f"{user.username} ({user.first_name} {user.last_name or ''})"
    header = f"💡 Proposta de {user_display}: "

    # Send to the group preserving original formatting entities
    if msg.text:
        await context.bot.send_message(
            chat_id=GROUP_PROPOSALS,
            text=header + user_text,
            entities=shift_entities(msg.entities, header),
        )
    else:
        await context.bot.copy_message(
            chat_id=GROUP_PROPOSALS,
            from_chat_id=msg.chat_id,
            message_id=msg.message_id,
            caption=header + user_text,
            caption_entities=shift_entities(msg.caption_entities, header),
        )

async def handle_edited_proposal(update, context, is_proposal):
    msg = update.effective_message
    user_text = (msg.text or msg.caption or "")

    # Confirmation with edit-specific message
    await msg.reply_text(random.choice(TEXT_REPLY_EDITED_PROPOSAL))

    # Header to identify the author and mark the message as edited
    user = msg.from_user
    user_display = f"{user.username} ({user.first_name} {user.last_name or ''})"
    header = f"✏️ Proposta editada de {user_display}: "

    if msg.text:
        await context.bot.send_message(
            chat_id=GROUP_PROPOSALS,
            text=header + user_text,
            entities=shift_entities(msg.entities, header),
        )
    else:
        await context.bot.copy_message(
            chat_id=GROUP_PROPOSALS,
            from_chat_id=msg.chat_id,
            message_id=msg.message_id,
            caption=header + user_text,
            caption_entities=shift_entities(msg.caption_entities, header),
        )

async def handle_netflix_mention(msg):
    """Replies with a random Netflix-themed comment."""
    await msg.reply_text(random.choice(TEXT_REPLY_NETFLIX))


async def handle_palasaca(msg):
    """Handles thank-you replies and GIFs."""
    # Note: PALASACA is already filtered in main, this is an extra safety check.
    
    if random.random() % 2 == 0:
        await msg.reply_text(random.choice(TEXT_REPLY_PALASACA))
    else:
        gif = get_giphy_url(["thank you", "cute cat", "love animal"])
        if gif: 
            await msg.reply_animation(gif)
        else:
            # Fallback in case the GIF fetch fails
            await msg.reply_text(random.choice(TEXT_REPLY_PALASACA))

from telegram import Update, MessageEntity, constants
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from constants import TAG_AMAZON, TEXT_REPLY_AFILIATS_LINK
import requests
import random

async def handle_amazon_links(msg):
    """
    High-level function called from main.
    Detects, processes and replies to Amazon links.
    """
    replies = await add_afiliats_tag(msg)
    if replies:
        intro_text = random.choice(TEXT_REPLY_AFILIATS_LINK)
        for text, entity in replies:
            await msg.reply_text(intro_text)
            await msg.reply_text(text, entities=[entity])
        return True # Signal that the message was processed
    return False

def get_real_url_from_shortlink(url):
    try:
        resp = requests.get(url, timeout=5)
        return resp.url
    except:
        return url

async def add_afiliats_tag(message):
    """Extracts links, resolves short URLs and appends the affiliate tag."""
    url_entities_dict = message.parse_entities(types=[MessageEntity.URL, MessageEntity.TEXT_LINK])
    link_replies = []
    
    for entity, value in url_entities_dict.items():
        url_to_process = value if entity.type == MessageEntity.URL else entity.url
        
        # Only process Amazon links that don't already have the affiliate tag
        if any(dom in url_to_process.lower() for dom in ['amazon.es', 'amazon.com', 'amzn.eu']):
            if TAG_AMAZON not in url_to_process.lower():
                long_url = get_real_url_from_shortlink(url_to_process)
                link_reply = long_url + TAG_AMAZON
                
                new_entity = MessageEntity(
                    type=constants.MessageEntityType.URL,
                    offset=0,
                    length=len(link_reply),
                    url=long_url
                )
                link_replies.append((link_reply, new_entity))
    return link_replies


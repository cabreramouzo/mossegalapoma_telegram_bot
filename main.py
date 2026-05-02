import logging
import random
import functions_framework
from telegram import Update, MessageEntity, constants
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from constants import *
from amazon import handle_amazon_links
from handlers import handle_direct_proposal, handle_edited_proposal, handle_reply_proposal, handle_palasaca
from utils import get_giphy_url

# --- INITIALIZATION ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Global application instance - lazily initialized on first request
_application = None

def get_application():
    """Build and configure the application once per process instance."""
    global _application
    if _application is None:
        _application = Application.builder().token(TELEGRAM_TOKEN).build()
        _application.add_handler(MessageHandler(filters.TEXT | filters.CAPTION, main_handler))
    return _application

async def hora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Replies with the current date and time."""
    from datetime import datetime
    now = datetime.now()
    await update.effective_message.reply_text(
        f"Ara són les {now.strftime('%H:%M')} del {now.strftime('%d/%m/%Y')}"
    )

async def main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Single handler that manages all hashtag and link logic."""
    msg = update.effective_message
    if not msg or not (msg.text or msg.caption):
        return

    user_text = (msg.text or msg.caption or "")
    user_text_low = user_text.lower()
    user = msg.from_user
    
    # User identification for forwarding
    user_display = f"{user.username} ({user.first_name} {user.last_name or ''})"
    forward_header = f"{user_display}: "

    # 1. Amazon logic (links without affiliate tag)
    if any(dom in user_text_low for dom in ['amazon.es', 'amazon.com', 'amzn.eu']):
        await handle_amazon_links(msg)

    # 2. Proposal and errata logic
    is_proposal = any(h in user_text_low for h in HASHTAGS_PROPOSTA)
    is_errata = any(h in user_text_low for h in FEDERRATES)

    if is_proposal or is_errata:
        if update.edited_message:
            # CASE EDIT: The message was edited, re-process with edit-specific handler
            await handle_edited_proposal(update, context, is_proposal)
        elif msg.reply_to_message:
            # CASE A: It is a reply to another message
            await handle_reply_proposal(update, context, is_proposal)
        else:
            # CASE B: The hashtag is in the same message as the proposal
            await handle_direct_proposal(update, context, is_proposal)

    # 3. Gifts / Palasaca logic
    if any(h in user_text_low for h in PALASACA):
        await handle_palasaca(msg)

    # 4. Mandalorian easter egg
    if any(h in user_text_low for h in THIS_IS_THE_WAY):
        gif = get_giphy_url(["baby yoda", "mandalorian", "thisistheway"])
        if gif: await msg.reply_animation(gif)

# --- HANDLER REGISTRATION ---
# Handlers are registered inside get_application() on first call.

# --- WEBHOOK MANAGEMENT (Cloud Functions) ---
async def process_update(data):
    # async with app: handles initialize() and shutdown() - PTB recommended for serverless
    async with get_application() as app:
        update = Update.de_json(data, app.bot)
        await app.process_update(update)

@functions_framework.http
def webhook(request):
    """Entry point for Google Cloud Function"""
    if request.method == 'POST':
        try:
            import asyncio
            data = request.get_json(force=True)
            asyncio.run(process_update(data))
        except Exception as e:
            logger.exception("Error processing update: %s", e)
            return 'error', 500
    return 'ok'

# --- LOCAL EXECUTION ---
if __name__ == '__main__':
    import asyncio
    if not G_CLOUD:
        print("Bot running (Local mode - Polling)...")
        get_application().run_polling()
    else:
        print("G_CLOUD is set to True. Set it to False to run locally.")
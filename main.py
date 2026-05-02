import os
import logging
import random
import asyncio
import datetime
import requests
import json
import telegram
from telegram import Update, MessageEntity, constants
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- CONFIGURACIÓN Y CONSTANTES ---
INTERNAL_VERSION = '2.1'
G_CLOUD = True  # Cambiar a False para local

GROUP_PROPOSALS = -1001928595896
TAG_AMAZON = '&tag=pempins-21'
TENOR_API_KEY = os.environ.get("TENOR_API_KEY")
TELEGRAM_TOKEN = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])

# Emojis (Mantenidos como los tenías)
rocket, closed_mailbox, postbox, paperclip = '🚀', '📬', '📮', '📎'
biceps, grinning, winking, robot = '💪', '😁', '😉', '🤖'
thinking, fire, money_bag, siren = '🤔', '🔥', '💰', '🚨'
# ... (el resto se usan directamente abajo para legibilidad)

# --- LISTAS DE RESPUESTAS (Tu lógica original intacta) ---
HASHTAGS_PROPOSTA = [
    '#propostamossegui', '#proposta', '#propostesmossegui', '#propostesmosseguis',
    '#propostamosseguis', '#propostamosegui', '#propostamoseguis', '#propostesmosegui',
    '#propostesmoseguis'
]
FEDERRATES = ['#federrates', '#federrades', '#federates', "fe d'errates"]
PALASACA = [
    '#palasaca', '#amazon', '#palasaka', '#afiliats', 'compra per afiliats', 
    'compra feta per afiliats', 'comprat via afiliats', 'compra via afiliats'
]
THIS_IS_THE_WAY = ['#thisistheway', '#thiswastheway', '#aquesteselcami', '#mandalorian']

TEXT_REPLY_PROPOSAL = [
    f"Anoto la proposta! 💪", f"Proposta anotada 😉", f"Els hi anoto la proposta 😁",
    f"L'apunto! 📬", f"Els la deixo al guió 📮", f"Apuntada! 📎", 
    f"Viatjant cap al guió... 🚀", f"Clar que sí! 🤖", f"Fot-li! 😜"
]

TEXT_REPLY_PALASACA = [
    f"En @tomasmanz i tot l'equip t'estem molt agraïts! 😘",
    f"Gràcies! Cada dia estem més aprop del Tesla Model S... 😜",
    f"La targeta fot fum!!! 🔥💨", f"De mica en mica s'omple la pica! 🚰💰"
]

TEXT_REPLY_AFILIATS_LINK = [
    f"M'ha semblat veure un link d'Amazon sense afiliats 🤔: ",
    f"Gràcies per recomanar un producte! Li afegeixo l'enllaç d'afiliats 😜: ",
    f"Amazon? Afiliats!!! 🔥💰: ", f"Enllaç d'afiliats al canto! 🚨: "
]

# --- INICIALIZACIÓN ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Instancia global de la aplicación
application = Application.builder().token(TELEGRAM_TOKEN).build()

# --- FUNCIONES DE APOYO ---

async def hora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    missatge = str(datetime.datetime.now())
    await update.effective_message.reply_text(text=missatge)

def get_real_url_from_shortlink(url):
    try:
        resp = requests.get(url, timeout=5)
        return resp.url
    except:
        return url

def get_tenor_url(search_terms):
    apikey = TENOR_API_KEY
    search_term = random.choice(search_terms)
    try:
        r = requests.get(f"https://api.tenor.com/v1/search?q={search_term}&key={apikey}&limit=4&media_filter=minimal", timeout=5)
        if r.status_code == 200:
            gifs = r.json()
            return random.choice(gifs['results'])['url']
    except:
        pass
    return None

# --- LÓGICA CORE (Refactorizada pero respetando tu funcionamiento) ---

async def add_afiliats_tag(message):
    """Extrae links, los resuelve y añade el tag."""
    url_entities_dict = message.parse_entities(types=[MessageEntity.URL, MessageEntity.TEXT_LINK])
    link_replies = []
    
    for entity, value in url_entities_dict.items():
        url_to_process = value if entity.type == MessageEntity.URL else entity.url
        
        # Solo procesamos si es Amazon y NO tiene ya el tag
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


async def handle_reply_proposal(update, context, is_proposal):
    msg = update.effective_message
    target_msg = msg.reply_to_message
    content_text = (target_msg.text or target_msg.caption or "")
    
    # Confirmación en el grupo
    await msg.reply_text(random.choice(TEXT_REPLY_PROPOSAL) if is_proposal else "Anoto la fe d'errates! 📝")

    # PASO 1: Copia exacta del original (Foto, video o texto)
    sent_msg = await context.bot.copy_message(
        chat_id=GROUP_PROPOSALS,
        from_chat_id=target_msg.chat_id,
        message_id=target_msg.message_id
    )

    # PASO 2: Info del fichaje + Comentario del moderador
    orig_user = target_msg.from_user
    orig_display = f"{orig_user.username} ({orig_user.first_name})"
    
    info_text = (
        f"💡 **Proposta de:** {orig_display}\n"
        f"👤 **Fichada por:** @{msg.from_user.username}\n"
        f"💬 **Comentario:** {msg.text or msg.caption}"
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
    
    if is_proposal and len(user_text) < 10:
        await msg.reply_text(f"Això no té pinta de proposta... 😒")
        return

    # Confirmación
    await msg.reply_text(random.choice(TEXT_REPLY_PROPOSAL) if is_proposal else "Anoto la fe d'errates! 📝")

    # Header para identificar al autor
    user = msg.from_user
    user_display = f"{user.username} ({user.first_name})"
    header = f"💡 **Proposta de {user_display}:**\n\n"

    # Enviamos al grupo (copy_message funciona para fotos y texto)
    # Si es solo texto, Telegram ignora el 'caption', así que usamos una lógica simple:
    if msg.text:
        await context.bot.send_message(
            chat_id=GROUP_PROPOSALS,
            text=header + user_text,
            parse_mode="Markdown"
        )
    else:
        await context.bot.copy_message(
            chat_id=GROUP_PROPOSALS,
            from_chat_id=msg.chat_id,
            message_id=msg.message_id,
            caption=header + user_text,
            parse_mode="Markdown"
        )

async def main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler único que gestiona la lógica de hashtags y links."""
    msg = update.effective_message
    if not msg or not (msg.text or msg.caption):
        return

    user_text = (msg.text or msg.caption or "")
    user_text_low = user_text.lower()
    user = msg.from_user
    
    # Identificación del usuario para el reenvío
    user_display = f"{user.username} ({user.first_name} {user.last_name or ''})"
    forward_header = f"{user_display}: "

    # 1. Lógica de Amazon (Links sin hashtag)
    if any(dom in user_text_low for dom in ['amazon.es', 'amazon.com', 'amzn.eu']):
        replies = await add_afiliats_tag(msg)
        if replies:
            intro_text = random.choice(TEXT_REPLY_AFILIATS_LINK)
            for text, entity in replies:
                await msg.reply_text(intro_text)
                await msg.reply_text(text, entities=[entity])

    # 2. Lógica de Proposiciones y Erratas
    is_proposal = any(h in user_text_low for h in HASHTAGS_PROPOSTA)
    is_errata = any(h in user_text_low for h in FEDERRATES)

    if is_proposal or is_errata:

        if msg.reply_to_message:
            # CASO A: Es una respuesta a otro mensaje
            await handle_reply_proposal(update, context, is_proposal)
        else:
            # CASO B: El hashtag va en el mismo mensaje que la propuesta
            await handle_direct_proposal(update, context, is_proposal)

    # 3. Lógica de Regalos / Palasaca
    if any(h in user_text_low for h in PALASACA):
        if random.random() > 0.5: # 50% de probabilidad como tu random_number%2
            await msg.reply_text(random.choice(TEXT_REPLY_PALASACA))
        else:
            gif = get_tenor_url(["thank you", "cute cat", "love animal"])
            if gif: await msg.reply_animation(gif)

    # 4. Mandalorian
    if any(h in user_text_low for h in THIS_IS_THE_WAY):
        gif = get_tenor_url(["baby yoda", "mandalorian", "thisistheway"])
        if gif: await msg.reply_animation(gif)

# --- REGISTRO DE HANDLERS ---
# Usamos un filtro amplio para que main_handler gestione todo (texto, fotos con caption, etc.)
application.add_handler(MessageHandler(filters.TEXT | filters.CAPTION, main_handler))

# --- GESTIÓN DE WEBHOOK (Cloud Functions) ---
async def process_update(data):
    async with application:
        update = Update.de_json(data, application.bot)
        await application.process_update(update)

def webhook(request):
    """Punto de entrada para Google Cloud Function"""
    if request.method == 'POST':
        data = request.get_json(force=True)
        # En CF usamos un loop de eventos para la corrutina
        asyncio.run(process_update(data))
    return 'ok'

# --- EJECUCIÓN LOCAL (Tu lógica G_CLOUD) ---
if __name__ == '__main__':
    if not G_CLOUD:
        print("Bot en marcha (Modo Local - Polling)...")
        application.run_polling()
    else:
        print("G_CLOUD está en True. Si quieres ejecutar en local, cámbialo a False.")
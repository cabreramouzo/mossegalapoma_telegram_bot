import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import logging
import os
import random
import requests
import json

from hashtags import HT_PROPOSTES, HT_FEDERATES, HT_PALASACA, HT_THISISTHEWAY
from replies import text_troll_reply, text_reply_proposal, text_reply_errata, text_reply_palasaca, text_rich_reply_proposal_netflix, text_rich_reply_proposal_hbo, text_rich_reply_proposal_disney_plus
from emoji_unicode import *


INTERNAL_VERSION = '1.0.5'
G_CLOUD = True
''' If the bot is hosted in Google Cloud Function set this constant to True. If false
the bot will run using a busy waiting technique'''

#bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
#tenor_api_key = os.environ["TENOR_API_KEY"]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def message_for_thuesday(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=-291751171, 
                            text="*Propostes d'aquesta setmana*:", 
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
                            

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(update, bot):
    bot.send_message(chat_id=update.effective_chat.id, text="Hola! Sóc un bot bàsic per a mossegalapoma!.")

def help(update, bot):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sóc un bot amb comandes /start, /help i /hora.")


def hora(update, bot):
    missatge = str(datetime.datetime.now())
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=missatge)

def unknown(update, bot):
    bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text="Perdona però no entenc aquesta comanda 🤨")

def get_thanks_gif_url():
    # set the apikey and limit
    apikey = tenor_api_key
    lmt = 4

    # our test search
    search_term_list = ["cute cat", "kitty love", "love animal", "thank you", "cute animal", "love you" ]
    random_index_search_term = random.randint(0, len(search_term_list) -1)
    search_term = search_term_list[random_index_search_term]

    # get random results using default locale of EN_US
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&media_filter=minimal" % (search_term, apikey, lmt))
    url='https://tenor.com/view/funny-animals-cat-love-cat-hug-gif-14233808'
    if r.status_code == 200:
        gifs = json.loads(r.content)
        #print (gifs)
        random_index = random.randint(0, len(gifs) -1)
        url = gifs['results'][random_index]['url']

    return url

def get_mandalorian_gif_url():
    # set the apikey and limit
    apikey = tenor_api_key
    lmt = 4

    # our test search
    search_term_list = ["baby yoda", "baby yoda happy", "mandalorian", "thisistheway"]
    random_index_search_term = random.randint(0, len(search_term_list) -1)
    search_term = search_term_list[random_index_search_term]

    # get random results using default locale of EN_US
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&media_filter=minimal" % (search_term, apikey, lmt))
    url='https://tenor.com/view/baby-yoda-baby-yoda-happy-laughing-smile-happy-gif-16061896'
    if r.status_code == 200:
        gifs = json.loads(r.content)
        #print (gifs)
        random_index = random.randint(0, len(gifs) -1)
        url = gifs['results'][random_index]['url']

    return url

def split_user_message_info(update):
    user_text = update.effective_message.text
    telegram_user = update.effective_message.from_user
    user_name = ""
    user_first_name = "sense_nom"
    user_last_name = ""

    if telegram_user.username:
        user_name = telegram_user.username
    if telegram_user.first_name:
        user_first_name = telegram_user.first_name
    if telegram_user.last_name:
        user_last_name = telegram_user.last_name

    return (user_name, user_first_name, user_last_name, user_text)

def add_username_to_proposal_reply(user_name, replies):
    
    replies.append(f"Saps @{user_name}, jo també ho anava a proposar... {grinning_face_smiling_eyes}")
    replies.append(f"A veure, @{user_name}. Aquesta és bona {winking_face}")
    replies.append(f"@{user_name}, seguim endavant gràcies a tu {face_blowing_a_kiss}")
    replies.append(f"@{user_name}, sense tu això no seria possible {face_blowing_a_kiss}")
    replies.append(f"@{user_name}, necessitem mosseguis com tu per tirar això endavant. Merci! {grinning_face_smiling_eyes}")
    replies.append(f"Quan tinguem el Tesla, @{user_name} seràs dels primers a provar-lo! {sun_glasses} Paraula de Bot {robot}")
    replies.append(f"@{user_name}, saps que en @tomasmanz t'estima molt, oi? Jo en canvi... és complicat. {robot}")

    return replies

def generate_random_index_for_reply(reply_type):
    
    randint = 0

    if reply_type == 'proposta':
        randint = random.randint(0, len(text_reply_proposal) -1 )
    elif reply_type == 'errata':
        randint = random.randint(0, len(text_reply_errata) -1 )
    elif reply_type == 'troll':
        randint = random.randint(0, len(text_troll_reply) -1 )
    elif reply_type == 'netflix':
        randint = random.randint(0, len(text_rich_reply_proposal_netflix) -1 )
    elif reply_type == 'hbo':
        randint = random.randint(0, len(text_rich_reply_proposal_hbo) -1 )
    elif reply_type == 'disney_plus':
        randint = random.randint(0, len(text_rich_reply_proposal_disney_plus) -1 )
    elif reply_type == 'palasaca':
        randint = random.randint(0, len(text_reply_palasaca) -1 )
    
    return randint

def find_hashtags_and_send_response(user_name, user_first_name, user_last_name, user_text):

    if user_name != "":
        text_reply_proposal = add_username_to_proposal_reply(user_name, text_reply_proposal)
        

    #Add rich response if there is 'serie' or 'sèrie' or 'Netflix' in the message
    #message_keywords = ['netflix', 'sèrie', 'serie', 'peli']
    is_rich_response_netflix = False
    message_keywords_netflix = ['netflix', 'nètflix']
    if any( keyword for keyword in message_keywords_netflix if keyword in user_text.lower() ):
        is_rich_response_netflix = True
        
    text_reply_errata = [
        "Una altra vegada!?","Deixa'm apostar: Ha estat en Ludo ¬¬",
        "Sort en tenim de vosaltres!", "Una altra!? Anoto la fe d'errates!"
    ]
    
    random_troll_text_index = random.randint(0, len(text_troll_reply) -1 )
    random_rich_proposal_text_index_netflix = random.randint(0, len(text_rich_reply_proposal_netflix) -1 )
    random_rich_proposal_text_index_hbo = random.randint(0, len(text_rich_reply_proposal_hbo) -1 )
    random_rich_proposal_text_index_disney_plus = random.randint(0, len(text_rich_reply_proposal_disney_plus) -1 )
    random_proposal_text_index = random.randint(0, len(text_reply_proposal) -1 )
    random_errata_text_index = random.randint(0, len(text_reply_errata) -1 )
    random_palasaca_text_index = random.randint(0, len(text_reply_palasaca) -1 )

    text_troll = text_troll_reply[random_troll_text_index]

    if is_rich_response_netflix:
        text_proposal = text_rich_reply_proposal_netflix[random_rich_proposal_text_index_netflix]
    elif is_rich_response_hbo:
        text_proposal = text_rich_reply_proposal_hbo[random_rich_proposal_text_index_hbo]
    elif is_rich_response_disney_plus:
        text_proposal = text_rich_reply_proposal_disney_plus[random_rich_proposal_text_index_disney_plus]
    else:
        text_proposal = text_reply_proposal[random_proposal_text_index]
    
    text_errata = text_reply_errata[random_errata_text_index]

    text_palasaca = text_reply_palasaca[random_palasaca_text_index]

    def send_message(bot, to, message_to_reply, message):

        bot.send_message(chat_id=to, reply_to_message_id=message_to_reply, text=message)


    def look_for_hashtags_and_send_response(bot, update, user_text):

        if any(hashtag for hashtag in HT_PROPOSTES if hashtag in user_text.lower()):

            if len(user_text) < 20:
                send_message(bot=bot, to=update.effective_chat.id, message_to_reply=update.effective_message.message_id, text=text_troll)
            else:
                bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, text=text_proposal)
                bot.send_message(chat_id=-291751171, text=user_name + "("+ user_first_name + " " + user_last_name + "): " + user_text)

        if any(hashtag for hashtag in HT_FEDERATES if hashtag in user_text.lower()):
            bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, text=text_errata)
            bot.send_message(chat_id=-291751171, text=user_name + "("+ user_first_name + " " + user_last_name + "): " + user_text)

        #afiliats
        if any(hashtag for hashtag in HT_PALASACA if hashtag in user_text.lower()):
            random_number = random.randint(0,10)
            if random_number%2 == 0:
                bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, text=text_palasaca)
            else:
                url = get_thanks_gif_url()
                bot.send_animation(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, animation=url)

        #mandalorian
        if any(hashtag for hashtag in HT_THISISTHEWAY if hashtag in user_text.lower()):
            url = get_mandalorian_gif_url()
            bot.send_animation(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, animation=url)

def filter_hashtag_messages(update, bot):
    #user text
    if update is not None and update.effective_message.text is not None:
        
        user_name, user_first_name, user_last_name, user_text = split_user_message_info(update)

        

#based in https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
# def webhook(request):
#     bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
#     if request.method == 'POST':
#         update = telegram.Update.de_json(request.get_json(force=True), bot)

#         filter_hashtag_messages(update, bot)
#     return 'ok'

# updater = Updater(token=os.environ["TELEGRAM_TOKEN"], use_context=True)
# job_queue = updater.job_queue

# thuesday_at_14 = datetime.time(hour=16, minute=0, second=0)
# job_thuesday = job_queue.run_daily(message_for_thuesday, time=thuesday_at_14, days= (1,))
# job_queue.start()

# if not G_CLOUD:
#     dispatcher = updater.dispatcher

#     #dispatcher.add_handler(CommandHandler('start', start))
#     #dispatcher.add_handler(CommandHandler('help', help))
#     #dispatcher.add_handler(CommandHandler('hora', hora))

#     unknown_handler = MessageHandler(Filters.command, unknown)
#     dispatcher.add_handler(unknown_handler)

#     dispatcher.add_handler(MessageHandler(Filters.entity("hashtag"), filter_hashtag_messages))

#     updater.start_polling()